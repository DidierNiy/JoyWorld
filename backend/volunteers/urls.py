from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VolunteerOpportunityViewSet, VolunteerApplicationViewSet, VolunteerHoursViewSet
)

router = DefaultRouter()
router.register(r'opportunities', VolunteerOpportunityViewSet)
router.register(r'applications', VolunteerApplicationViewSet)
router.register(r'hours', VolunteerHoursViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
