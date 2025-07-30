from rest_framework import serializers
from .models import DonationCampaign, Donation, DonationReceipt

class DonationCampaignSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    
    class Meta:
        model = DonationCampaign
        fields = [
            'id', 'title', 'description', 'short_description',
            'goal_amount', 'raised_amount', 'image', 'status',
            'start_date', 'end_date', 'progress_percentage', 
            'is_completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'raised_amount', 'created_at', 'updated_at']

class DonationSerializer(serializers.ModelSerializer):
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    
    class Meta:
        model = Donation
        fields = [
            'id', 'campaign', 'campaign_title', 'donor_name', 'donor_email',
            'donor_phone', 'amount', 'payment_method', 'payment_status',
            'transaction_id', 'payment_intent_id', 'paypal_order_id',
            'is_anonymous', 'message', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'payment_status', 'transaction_id', 'payment_intent_id',
            'paypal_order_id', 'created_at', 'updated_at'
        ]

class DonationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating donations"""
    class Meta:
        model = Donation
        fields = [
            'campaign', 'donor_name', 'donor_email', 'donor_phone',
            'amount', 'payment_method', 'is_anonymous', 'message'
        ]

class DonationReceiptSerializer(serializers.ModelSerializer):
    donation_details = DonationSerializer(source='donation', read_only=True)
    
    class Meta:
        model = DonationReceipt
        fields = [
            'id', 'donation', 'donation_details', 'receipt_number',
            'pdf_file', 'generated_at'
        ]
        read_only_fields = ['id', 'receipt_number', 'generated_at']

class DonationStatsSerializer(serializers.Serializer):
    """Serializer for donation statistics"""
    total_donations = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_donors = serializers.IntegerField()
    average_donation = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_donations = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    recent_donations = DonationSerializer(many=True, read_only=True)
