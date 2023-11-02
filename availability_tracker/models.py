from django.db import models
from datetime import timedelta
from django.db import IntegrityError

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Availability(models.Model):
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='availabilities')
    timestamp = models.DateTimeField()
    is_data = models.BooleanField(default=False)
    nominal_timestamp = models.DateTimeField()
    daily_availability = models.FloatField(null=True, blank=True)
    hourly_availability = models.FloatField(null=True, blank=True)
    monthly_availability = models.FloatField(null=True, blank=True)
    campaign_availability = models.FloatField(null=True, blank=True)
    height = models.FloatField()

    def __str__(self):
        return f"Daily {self.daily_availability}, Monthly {self.monthly_availability}, Campaign {self.campaign_availability}"

    class Meta:
        verbose_name_plural = "Availabilities"

class LidarMeasurement(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='lidar_measurements')
    timestamp = models.DateTimeField()
    height = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - Height: {self.height}, Wind Speed: {self.wind_speed}"
