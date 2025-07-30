from django.contrib import admin
from django.utils.html import format_html
from .models import DonationCampaign, Donation, DonationReceipt

@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal_amount', 'raised_amount', 'progress_bar', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'raised_amount', 'progress_percentage', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('title', 'short_description', 'description', 'image')
        }),
        ('Financial Details', {
            'fields': ('goal_amount', 'raised_amount', 'progress_percentage')
        }),
        ('Status & Dates', {
            'fields': ('status', 'start_date', 'end_date')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def progress_bar(self, obj):
        percentage = obj.progress_percentage
        color = 'green' if percentage >= 100 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">' +
            '<div style="width: {}px; background-color: {}; height: 20px; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">{:.1f}%</div>' +
            '</div>',
            min(percentage, 100), color, percentage
        )
    progress_bar.short_description = 'Progress'

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'campaign', 'amount', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'payment_method', 'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'campaign__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('campaign', 'amount', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'payment_intent_id', 'paypal_order_id')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('campaign')

@admin.register(DonationReceipt)
class DonationReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'donation_donor', 'donation_amount', 'generated_at']
    list_filter = ['generated_at']
    search_fields = ['receipt_number', 'donation__donor_name', 'donation__donor_email']
    readonly_fields = ['id', 'receipt_number', 'generated_at']
    ordering = ['-generated_at']
    
    def donation_donor(self, obj):
        return obj.donation.donor_name
    donation_donor.short_description = 'Donor'
    
    def donation_amount(self, obj):
        return f'${obj.donation.amount}'
    donation_amount.short_description = 'Amount'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('donation')
