from django.contrib import admin
from .models import Availability, Campaign, LidarMeasurement

admin.site.register(Campaign)
admin.site.register(Availability)
admin.site.register(LidarMeasurement)
