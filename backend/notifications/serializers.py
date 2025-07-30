from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient_email', 'title', 'message',
            'notification_type', 'is_read', 'reference_id',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    class Meta:
        model = Notification
        fields = [
            'recipient_email', 'title', 'message',
            'notification_type', 'reference_id'
        ]
