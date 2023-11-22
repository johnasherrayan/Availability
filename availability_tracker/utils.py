from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from .serializers import AvailabilitySerializer
import logging
from .models import Availability
import os
import boto3
import requests
from dotenv import load_dotenv
import json



logger = logging.getLogger(__name__)
load_dotenv()

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

            first_timestamp = Availability.objects.filter(campaign_id=campaign_id, campaign_availability__isnull=False).order_by('timestamp').first()

            last_timestamp = Availability.objects.filter(campaign_id=campaign_id, campaign_availability__isnull=False).order_by('-timestamp').first()

            if first_timestamp is not None and last_timestamp is not None:
                calculate_total_days = calculate_total_possible_days(first_timestamp.timestamp, last_timestamp.timestamp)

            timestamp = datetime.fromisoformat(timestamp)
            non_null_count = Availability.objects.filter(campaign_id=campaign_id, timestamp__gte=first_timestamp.timestamp, timestamp__lte=last_timestamp.timestamp, campaign_availability__isnull=False).count()

            total_possible_points = calculate_total_days * 144
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


def calculate_total_possible_days(start_timestamp, end_timestamp):
    total_possible_days = (end_timestamp - start_timestamp).days + 1
    return total_possible_days


def read_data_from_aws_s3():  
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
    aws_object_key = os.getenv('AWS_OBJECT_KEY')
    aws_region_name = os.getenv('AWS_REGION_NAME')
    
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                  aws_secret_access_key=aws_secret_key, region_name=aws_region_name)
    try:
        url = s3.generate_presigned_url('get_object', Params={'Bucket': aws_bucket_name, 'Key': aws_object_key})

        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



        
        

