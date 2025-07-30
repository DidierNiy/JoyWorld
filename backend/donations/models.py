from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class DonationCampaign(models.Model):
    """Model for donation campaigns/causes"""
    CAMPAIGN_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('draft', 'Draft'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.CharField(max_length=500, blank=True, null=True, help_text='Image URL or path')
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return min((self.raised_amount / self.goal_amount) * 100, 100)
        return 0
    
    @property
    def is_completed(self):
        return self.raised_amount >= self.goal_amount

class Donation(models.Model):
    """Model for individual donations"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD = [
        ('stripe', 'Credit/Debit Card (Stripe)'),
        ('paypal', 'PayPal'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(DonationCampaign, on_delete=models.CASCADE, related_name='donations')
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)  # For Stripe
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True)  # For PayPal
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        donor = 'Anonymous' if self.is_anonymous else self.donor_name
        return f'{donor} - ${self.amount} to {self.campaign.title}'

class DonationReceipt(models.Model):
    """Model for donation receipts/tax documents"""
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='receipts/', blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Receipt #{self.receipt_number} for {self.donation.donor_name}'
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate unique receipt number
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.receipt_number = f'JW-{timestamp}-{str(self.donation.id)[:8].upper()}'
        super().save(*args, **kwargs)
