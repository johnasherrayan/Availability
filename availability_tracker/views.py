from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Availability, Campaign, LidarMeasurement
from rest_framework import status
from .serializers import AvailabilitySerializer, CampaignSerializer, LidarMeasurementSerializer
from .utils import calculate_data_availability, get_none_availability_data
import pandas as pd

class CampaignDetailView(APIView):
    def get(self, request, id=None):
        if id is not None:
            campaign = get_object_or_404(Campaign, id=id)
            serializer = CampaignSerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            campaigns = Campaign.objects.all()
            serializer = CampaignSerializer(campaigns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        campaign = get_object_or_404(Campaign, id=id)
        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        campaign = get_object_or_404(Campaign, id=id)
        campaign.delete()
        return Response({'detail': 'Campaign deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class CampaignCreateView(APIView):
    def get(self, request):
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AvailabilityDetailView(APIView):
    def get(self, request, id=None):
        if id is not None:
            availability = get_object_or_404(Availability, id=id)
            serializer = AvailabilitySerializer(availability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            availability = Availability.objects.all()
            serializer = AvailabilitySerializer(availability, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        availability = get_object_or_404(Availability, id=id)
        serializer = AvailabilitySerializer(availability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        availability = get_object_or_404(Availability, id=id)
        availability.delete()
        return Response({'detail': 'Availability deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class AvailabilityCreateView(APIView):
    def get(self, request):
        try:
            latest_data = Availability.objects.all()
            response_data = AvailabilitySerializer(latest_data, many=True)
            return Response(response_data.data, status=status.HTTP_200_OK)
        except Availability.DoesNotExist:
            return Response({'detail': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = AvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailabilityCampaignDetailView(APIView):
    def get(self, request, campaign_id):
        try:
            availability_instance = Availability.objects.filter(campaign_id=campaign_id)
            availabilities = availability_instance.exclude(daily_availability=9999.0, monthly_availability=9999.0, campaign_availability=9999.0).count()
            
            timestamps = [availability.timestamp for availability in availability_instance]

            response_data = {
                'timestamp': timestamps,
                'dataAvailable': bool(availabilities)
            }

            if availabilities:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Availability.DoesNotExist:
            return Response({'detail': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

class LidarMeasurementListCreateView(APIView):
    def get(self, request, campaign_id=None, format=None):
        if campaign_id:
            measurements = LidarMeasurement.objects.filter(campaign_id=campaign_id)
        else:
            measurements = LidarMeasurement.objects.all()
        
        serializer = LidarMeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LidarMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvailabilityCalculateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            campaign_id = request.data.get('campaign_id')
            data_points = request.data.get('data', [])

            response_data = []
            availability_data = {} 

            start_timestamp = data_points[0]["timestamp"]
            end_timestamp = data_points[-1]["timestamp"]

            timestamps = [point["timestamp"] for point in data_points]

            nominal_timestamps = pd.date_range(start = start_timestamp , end = end_timestamp, freq='10T')
            nominal_timestamps_list = nominal_timestamps.strftime('%Y-%m-%dT%H:%M:%S').tolist()

            timestamps_set = set(timestamps)
            nominal_timestamps_set = set(nominal_timestamps_list)

            missing_timestamp = list(nominal_timestamps_set - timestamps_set)

            all_timestamps = sorted(data_points + [{"timestamp": ts} for ts in missing_timestamp], key=lambda x: x['timestamp'])

            for i, data_point in enumerate(all_timestamps):
                timestamp = data_point.get('timestamp')
                data_available = data_point.get('dataAvailable', False)
                height = data_point.get('height')

                if timestamp in missing_timestamp:
                    response_data.append(get_none_availability_data(campaign_id, timestamp))

                if data_available:
                    valid_data_points = height

                    for i in range(1, height+1):
                        daily_data_availability = calculate_data_availability(timestamp, valid_data_points, time_period='day')
                        hourly_data_availability = calculate_data_availability(timestamp, valid_data_points, time_period='hour')
                        monthly_availability = calculate_data_availability(timestamp, valid_data_points, time_period='month')
                        campaign_availability = 0

                        availability_data = {
                            'campaign_id': campaign_id,
                            'timestamp': timestamp,
                            'nominal_timestamp': timestamp,
                            'daily_availability': daily_data_availability,
                            'hourly_availability': hourly_data_availability,
                            'monthly_availability': monthly_availability,
                            'campaign_availability': campaign_availability,
                            'is_data': data_available,
                            'height': i
                        }

                        response_data.append(availability_data)
                        serializer = AvailabilitySerializer(data=availability_data)
                        if serializer.is_valid():
                            serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

