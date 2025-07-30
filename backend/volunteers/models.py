from django.db import models
from django.utils import timezone
import uuid

class VolunteerOpportunity(models.Model):
    """Model for volunteer opportunities"""
    OPPORTUNITY_TYPE = [
        ('one_time', 'One-time Event'),
        ('ongoing', 'Ongoing Opportunity'),
        ('seasonal', 'Seasonal'),
        ('emergency', 'Emergency Response'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('full', 'Full'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE)
    location = models.CharField(max_length=200)
    skills_required = models.TextField(help_text='List of skills or qualifications needed')
    time_commitment = models.CharField(max_length=100, help_text='e.g., 2 hours/week, One day')
    max_volunteers = models.PositiveIntegerField(help_text='Maximum number of volunteers needed')
    current_volunteers = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.CharField(max_length=500, blank=True, null=True, help_text='Image URL or path')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def spots_remaining(self):
        return max(0, self.max_volunteers - self.current_volunteers)
    
    @property
    def is_full(self):
        return self.current_volunteers >= self.max_volunteers

class VolunteerApplication(models.Model):
    """Model for volunteer applications"""
    APPLICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    AVAILABILITY = [
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('evenings', 'Evenings'),
        ('flexible', 'Flexible'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE, related_name='applications')
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    # Volunteer Information
    availability = models.CharField(max_length=20, choices=AVAILABILITY)
    previous_volunteer_experience = models.TextField(blank=True, null=True)
    skills_and_interests = models.TextField()
    why_volunteer = models.TextField(help_text='Why do you want to volunteer with us?')
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    # Background Check (if required)
    background_check_consent = models.BooleanField(default=False)
    background_check_completed = models.BooleanField(default=False)
    background_check_date = models.DateField(blank=True, null=True)
    
    # Application Status
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    notes = models.TextField(blank=True, null=True, help_text='Internal notes about the application')
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['opportunity', 'email']  # Prevent duplicate applications
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.opportunity.title}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class VolunteerHours(models.Model):
    """Model to track volunteer hours"""
    volunteer = models.ForeignKey(VolunteerApplication, on_delete=models.CASCADE, related_name='hours_logged')
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(help_text='Description of work performed')
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f'{self.volunteer.full_name} - {self.hours} hours on {self.date}'
