from django.db import models
from django.contrib.auth.models import User
import uuid

class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPE = [
        ('donation_received', 'Donation Received'),
        ('volunteer_application', 'Volunteer Application'),
        ('campaign_update', 'Campaign Update'),
        ('general_announcement', 'General Announcement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient_email = models.EmailField(help_text="Email of the recipient")
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE)
    is_read = models.BooleanField(default=False)
    reference_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID of the related object (e.g., Donation ID, Volunteer Application ID)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Notification for {self.recipient_email}: {self.title}"
