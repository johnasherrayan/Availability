from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from .serializers import AvailabilitySerializer
import logging
from .models import Availability


logger = logging.getLogger(__name__)

def calculate_data_availability(timestamp, valid_data_points, campaign_id, time_period='day'):
        
        if time_period == 'day':
            timestamp = datetime.fromisoformat(timestamp)
            date = timestamp.date()
            non_null_count = Availability.objects.filter(timestamp__date=date, daily_availability__isnull=False).count()

            total_possible_points = 144
            valid_points = valid_data_points + non_null_count

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability
        
        if time_period == 'hour':
            total_possible_points = 6
            valid_points = valid_data_points

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability

        if time_period == 'month':
            timestamp = datetime.fromisoformat(timestamp)
            month = timestamp.month
            year = timestamp.year
            non_null_count = Availability.objects.filter(timestamp__year=year, timestamp__month=month, monthly_availability__isnull=False).count()

            total_possible_points = 4320
            valid_points = valid_data_points + non_null_count

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability
        
        if time_period == 'campaign':
            timestamp = datetime.fromisoformat(timestamp)
            year = timestamp.year
            non_null_count = Availability.objects.filter(campaign_id=campaign_id, timestamp__year=year, campaign_availability__isnull=False).count()

            total_possible_points = 51840
            valid_points = valid_data_points + non_null_count

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability
        
def get_none_availability_data(campaign_id, missing_timestamp):
        nominal_timestamp = missing_timestamp
        none_availability_data = {
            'campaign_id': campaign_id,
            'timestamp': nominal_timestamp,
            'nominal_timestamp': nominal_timestamp,
        }

        for _ in range(1):
            none_availability_data['daily_availability'] = None
            none_availability_data['hourly_availability'] = None
            none_availability_data['monthly_availabilit'] = None
            none_availability_data['campaign_availability'] = None
            none_availability_data['height'] = 0

        none_availability_data['is_data'] = False
        serializer = AvailabilitySerializer(data=none_availability_data)
        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(f'Serializer errors: {serializer.errors}')
        return none_availability_data

        
        

