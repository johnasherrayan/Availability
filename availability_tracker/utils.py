from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta, date
from .serializers import AvailabilitySerializer
import logging


logger = logging.getLogger(__name__)

def calculate_data_availability(timestamp, valid_data_points, time_period='day', gap_threshold=timedelta(minutes=10)):
        
        if time_period == 'day':
            timestamp = datetime.fromisoformat(timestamp)
            start_of_day = datetime.combine(timestamp.date(), datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)

            total_possible_points = 144
            valid_points = valid_data_points

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability
        
        if time_period == 'hour':
            total_possible_points = 6
            valid_points = valid_data_points

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability

        if time_period == 'month':
            total_possible_points = 4320
            valid_points = valid_data_points

            data_availability = (valid_points / total_possible_points) * 100
            return data_availability
        
def get_none_availability_data(campaign_id, timestamp, height, average_time_diff):
        nominal_timestamp = timestamp + timedelta(minutes=average_time_diff)
        none_availability_data = {
            'campaign_id': campaign_id,
            'timestamp': nominal_timestamp,
            'nominal_timestamp': nominal_timestamp,
        }

        for _ in range(1, height + 1):
            none_availability_data['daily_availability'] = None
            none_availability_data['hourly_availability'] = None
            none_availability_data['monthly_availabilit'] = None
            none_availability_data['campaign_availability'] = None
            none_availability_data['height'] = height

        none_availability_data['is_data'] = False
        serializer = AvailabilitySerializer(data=none_availability_data)
        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(f'Serializer errors: {serializer.errors}')
        return none_availability_data


def calculate_average_time_difference(data_points):
    timestamps = [entry["timestamp"] for entry in data_points]
    datetime_objects = [datetime.fromisoformat(timestamp) for timestamp in timestamps]
    average_time_diff = sum([datetime_objects[i + 1] - datetime_objects[i] for i in range(len(datetime_objects) - 1)], timedelta()) / (len(datetime_objects) - 1)
    minutes, seconds = divmod(average_time_diff.seconds, 60)
    formatted_average_time_diff = minutes + seconds / 60.0

    return formatted_average_time_diff
        
        

