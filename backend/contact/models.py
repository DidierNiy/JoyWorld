from django.db import models
from django.utils import timezone
import uuid

class ContactMessage(models.Model):
    """Model for contact form submissions"""
    MESSAGE_TYPE = [
        ('general', 'General Inquiry'),
        ('donation', 'Donation Inquiry'),
        ('volunteer', 'Volunteer Inquiry'),
        ('partnership', 'Partnership'),
        ('media', 'Media Inquiry'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Response tracking
    response_message = models.TextField(blank=True, null=True)
    responded_by = models.CharField(max_length=100, blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.subject}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class EmailTemplate(models.Model):
    """Model for email templates"""
    TEMPLATE_TYPE = [
        ('donation_confirmation', 'Donation Confirmation'),
        ('donation_receipt', 'Donation Receipt'),
        ('volunteer_application_received', 'Volunteer Application Received'),
        ('volunteer_application_approved', 'Volunteer Application Approved'),
        ('volunteer_application_rejected', 'Volunteer Application Rejected'),
        ('contact_response', 'Contact Form Response'),
        ('newsletter', 'Newsletter'),
        ('campaign_update', 'Campaign Update'),
        ('general_notification', 'General Notification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPE, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(help_text='HTML content of the email')
    text_content = models.TextField(help_text='Plain text content of the email', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} ({self.template_type})'

class EmailLog(models.Model):
    """Model to log sent emails"""
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200)
    template_used = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    provider = models.CharField(max_length=50, help_text='Email provider used (e.g., SendGrid, SMTP)')
    provider_message_id = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    
    # Related object reference
    reference_type = models.CharField(max_length=50, blank=True, null=True, help_text='Type of related object (e.g., Donation, VolunteerApplication)')
    reference_id = models.CharField(max_length=100, blank=True, null=True, help_text='ID of related object')
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f'Email to {self.recipient_email} - {self.subject}'

class NewsletterSubscriber(models.Model):
    """Model for newsletter subscribers"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('unsubscribed', 'Unsubscribed'),
        ('bounced', 'Bounced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    unsubscribe_token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Preferences
    receive_donation_updates = models.BooleanField(default=True)
    receive_volunteer_updates = models.BooleanField(default=True)
    receive_general_updates = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        name = f'{self.first_name} {self.last_name}'.strip() if self.first_name or self.last_name else 'Anonymous'
        return f'{name} ({self.email})'
    
    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            import secrets
            self.unsubscribe_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
