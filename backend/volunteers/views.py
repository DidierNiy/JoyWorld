from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import VolunteerOpportunity, VolunteerApplication, VolunteerHours
from .serializers import (
    VolunteerOpportunitySerializer, VolunteerApplicationSerializer,
    VolunteerApplicationCreateSerializer, VolunteerHoursSerializer,
    VolunteerStatsSerializer
)
# Email service temporarily disabled for basic testing
# from contact.services.email_service import send_volunteer_application_received_email
from django.db.models import Sum, Count

class VolunteerOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Volunteer Opportunities"""
    queryset = VolunteerOpportunity.objects.filter(status='active').order_by('-start_date')
    serializer_class = VolunteerOpportunitySerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='completed')
    def completed_opportunities(self, request):
        completed = VolunteerOpportunity.objects.filter(status='completed').order_by('-end_date')
        serializer = self.get_serializer(completed, many=True)
        return Response(serializer.data)

class VolunteerApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Volunteer Applications"""
    queryset = VolunteerApplication.objects.all().order_by('-created_at')
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VolunteerApplicationCreateSerializer
        return VolunteerApplicationSerializer
    
    def perform_create(self, serializer):
        application = serializer.save()
        
        # Update volunteer count for the opportunity
        opportunity = application.opportunity
        opportunity.current_volunteers += 1
        opportunity.save()
        
        # Email confirmation temporarily disabled for basic testing
        # send_volunteer_application_received_email(application)
    
    @action(detail=False, methods=['get'], url_path='stats', permission_classes=[IsAuthenticated])
    def statistics(self, request):
        """Returns volunteer statistics for admin dashboard"""
        total_volunteers = VolunteerApplication.objects.filter(status='approved').count()
        active_opportunities = VolunteerOpportunity.objects.filter(status='active').count()
        total_hours = VolunteerHours.objects.aggregate(Sum('hours'))['hours__sum'] or 0
        recent_applications = VolunteerApplication.objects.order_by('-created_at')[:10]
        
        stats_data = {
            'total_volunteers': total_volunteers,
            'active_opportunities': active_opportunities,
            'total_hours_logged': total_hours,
            'recent_applications': VolunteerApplicationSerializer(recent_applications, many=True).data
        }
        
        return Response(stats_data)

class VolunteerHoursViewSet(viewsets.ModelViewSet):
    """ViewSet for Volunteer Hours"""
    queryset = VolunteerHours.objects.all().order_by('-date')
    serializer_class = VolunteerHoursSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can manage hours
