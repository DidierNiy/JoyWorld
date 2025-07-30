from rest_framework import serializers
from .models import VolunteerOpportunity, VolunteerApplication, VolunteerHours

class VolunteerOpportunitySerializer(serializers.ModelSerializer):
    spots_remaining = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = VolunteerOpportunity
        fields = [
            'id', 'title', 'description', 'short_description',
            'opportunity_type', 'location', 'skills_required',
            'time_commitment', 'max_volunteers', 'current_volunteers',
            'start_date', 'end_date', 'contact_person', 'contact_email',
            'contact_phone', 'status', 'image', 'spots_remaining',
            'is_full', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_volunteers', 'created_at', 'updated_at']

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    opportunity_title = serializers.CharField(source='opportunity.title', read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = VolunteerApplication
        fields = [
            'id', 'opportunity', 'opportunity_title', 'first_name', 'last_name',
            'full_name', 'email', 'phone', 'date_of_birth', 'address',
            'city', 'state', 'zip_code', 'availability',
            'previous_volunteer_experience', 'skills_and_interests',
            'why_volunteer', 'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'background_check_consent',
            'background_check_completed', 'background_check_date',
            'status', 'notes', 'reviewed_by', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'background_check_completed', 'background_check_date',
            'status', 'notes', 'reviewed_by', 'reviewed_at',
            'created_at', 'updated_at'
        ]

class VolunteerApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating volunteer applications"""
    class Meta:
        model = VolunteerApplication
        fields = [
            'opportunity', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'city', 'state', 'zip_code',
            'availability', 'previous_volunteer_experience',
            'skills_and_interests', 'why_volunteer', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship',
            'background_check_consent'
        ]

class VolunteerHoursSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source='volunteer.full_name', read_only=True)
    opportunity_title = serializers.CharField(source='opportunity.title', read_only=True)
    
    class Meta:
        model = VolunteerHours
        fields = [
            'id', 'volunteer', 'volunteer_name', 'opportunity',
            'opportunity_title', 'date', 'hours', 'description',
            'verified_by', 'verified_at', 'created_at'
        ]
        read_only_fields = ['id', 'verified_by', 'verified_at', 'created_at']

class VolunteerStatsSerializer(serializers.Serializer):
    """Serializer for volunteer statistics"""
    total_volunteers = serializers.IntegerField()
    active_opportunities = serializers.IntegerField()
    total_hours_logged = serializers.DecimalField(max_digits=10, decimal_places=2)
    recent_applications = VolunteerApplicationSerializer(many=True, read_only=True)
