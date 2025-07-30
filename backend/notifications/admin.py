from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient_email', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient_email', 'title', 'message', 'reference_id')
    readonly_fields = ('id', 'created_at')
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('title', 'message', 'notification_type')
        }),
        ('Recipient Information', {
            'fields': ('recipient_email',)
        }),
        ('Status & System Info', {
            'fields': ('is_read', 'reference_id', 'id', 'created_at')
        })
    )
