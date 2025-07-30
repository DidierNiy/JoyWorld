from django.contrib import admin
from .models import ContactMessage, EmailTemplate, EmailLog, NewsletterSubscriber

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'message_type', 'status', 'created_at']
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'subject']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'message_type')
        }),
        ('Status & Response', {
            'fields': ('status', 'response_message', 'responded_by', 'responded_at')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active', 'created_at']
    search_fields = ['name', 'subject', 'template_type']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_type', 'subject', 'is_active')
        }),
        ('Content', {
            'fields': ('html_content', 'text_content')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient_email', 'subject', 'status', 'provider', 'sent_at']
    list_filter = ['status', 'provider', 'sent_at']
    search_fields = ['recipient_email', 'subject', 'recipient_name']
    readonly_fields = ['id', 'sent_at']
    ordering = ['-sent_at']
    
    fieldsets = (
        ('Email Details', {
            'fields': ('recipient_email', 'recipient_name', 'subject')
        }),
        ('Status & Provider', {
            'fields': ('status', 'provider', 'provider_message_id', 'error_message')
        }),
        ('Template & Reference', {
            'fields': ('template_used', 'reference_type', 'reference_id')
        }),
        ('Tracking', {
            'fields': ('sent_at', 'opened_at', 'clicked_at')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('template_used')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'status', 'subscribed_at']
    list_filter = ['status', 'subscribed_at']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['id', 'subscribed_at', 'unsubscribed_at', 'unsubscribe_token']
    ordering = ['-subscribed_at']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'first_name', 'last_name', 'status')
        }),
        ('Preferences', {
            'fields': ('receive_donation_updates', 'receive_volunteer_updates', 'receive_general_updates')
        }),
        ('System Information', {
            'fields': ('id', 'subscribed_at', 'unsubscribed_at', 'unsubscribe_token'),
            'classes': ('collapse',)
        })
    )
