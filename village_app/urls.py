from django.urls import path
from .views import VillagePricingView

urlpatterns = [
    path('village-pricing/', VillagePricingView.as_view(), name='village_pricing')
]
