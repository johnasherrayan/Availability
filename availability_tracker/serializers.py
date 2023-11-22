from rest_framework.serializers import ModelSerializer
from .models import Availability, Campaign, LidarMeasurement

class AvailabilitySerializer(ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class LidarMeasurementSerializer(ModelSerializer):
    class Meta:
        model = LidarMeasurement
        fields = '__all__'