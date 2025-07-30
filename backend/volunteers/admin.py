from django.contrib import admin
from .models import VolunteerOpportunity, VolunteerApplication, VolunteerHours

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'opportunity_type', 'status', 'max_volunteers', 'current_volunteers', 'start_date']
    list_filter = ['opportunity_type', 'status', 'start_date']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['id', 'current_volunteers', 'created_at', 'updated_at']
    ordering = ['-start_date']
    
    fieldsets = (
        ('Opportunity Details', {
            'fields': ('title', 'description', 'short_description', 'image')
        }),
        ('Logistics', {
            'fields': ('opportunity_type', 'location', 'time_commitment', 'start_date', 'end_date')
        }),
        ('Volunteer Management', {
            'fields': ('max_volunteers', 'current_volunteers', 'skills_required', 'status')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'opportunity', 'status', 'created_at']
    list_filter = ['status', 'opportunity', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'opportunity__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 
                'date_of_birth', 'address', 'city', 'state', 'zip_code'
            )
        }),
        ('Volunteer Details', {
            'fields': (
                'opportunity', 'availability', 'previous_volunteer_experience',
                'skills_and_interests', 'why_volunteer'
            )
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Application Status & Review', {
            'fields': ('status', 'notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Background Check', {
            'fields': ('background_check_consent', 'background_check_completed', 'background_check_date')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('opportunity')

@admin.register(VolunteerHours)
class VolunteerHoursAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'opportunity', 'date', 'hours', 'verified_by']
    list_filter = ['date', 'opportunity', 'volunteer']
    search_fields = ['volunteer__first_name', 'volunteer__last_name', 'opportunity__title']
    readonly_fields = ['created_at']
    ordering = ['-date']
    
    fieldsets = (
        ('Log Details', {
            'fields': ('volunteer', 'opportunity', 'date', 'hours', 'description')
        }),
        ('Verification', {
            'fields': ('verified_by', 'verified_at')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('volunteer', 'opportunity')
