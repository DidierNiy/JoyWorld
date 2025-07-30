from rest_framework import serializers
from .models import ContactMessage, EmailTemplate, EmailLog, NewsletterSubscriber

class ContactMessageSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'subject', 'message', 'message_type', 'status',
            'response_message', 'responded_by', 'responded_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'response_message', 'responded_by',
            'responded_at', 'created_at', 'updated_at'
        ]

class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contact messages"""
    class Meta:
        model = ContactMessage
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'subject', 'message', 'message_type'
        ]

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class EmailLogSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template_used.name', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = '__all__'
        read_only_fields = ['id', 'sent_at']

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'
        read_only_fields = ['id', 'subscribed_at', 'unsubscribed_at', 'unsubscribe_token']

class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    """Serializer for subscribing to newsletter"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'first_name', 'last_name']

class NewsletterUnsubscribeSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
