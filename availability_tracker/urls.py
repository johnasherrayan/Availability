# urls.py
from django.urls import path
from .views import AvailabilityCreateView, AvailabilityCampaignDetailView, CampaignDetailView, CampaignCreateView, AvailabilityDetailView, LidarMeasurementListCreateView, AvailabilityCalculateView

urlpatterns = [
    path('campaign/', CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:id>', CampaignDetailView.as_view(), name='campaign-detail'),
    path('availability_campaign/<int:campaign_id>/', AvailabilityCampaignDetailView.as_view(), name='availability-campain-detail'),
    path('availability/', AvailabilityCreateView.as_view(), name='availability-create'),
    path('availability/<int:id>/', AvailabilityDetailView.as_view(), name='availability-detail'),
    path('create_lidar', LidarMeasurementListCreateView.as_view(), name='create_lidar'),
    path('availability_calculate/', AvailabilityCalculateView.as_view(), name='availability-calculate'),


]
