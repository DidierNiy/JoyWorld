from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import DonationCampaign, Donation
from .serializers import (
    DonationCampaignSerializer, DonationSerializer, 
    DonationCreateSerializer, DonationStatsSerializer
)
# Payment services temporarily disabled for basic testing
# from .services.stripe_service import create_stripe_payment_intent, handle_stripe_webhook
# from .services.paypal_service import create_paypal_payment, execute_paypal_payment
from django.db.models import Sum, Avg, Count
from django.utils import timezone

class DonationCampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Donation Campaigns"""
    queryset = DonationCampaign.objects.filter(status='active').order_by('-created_at')
    serializer_class = DonationCampaignSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='completed')
    def completed_campaigns(self, request):
        completed_campaigns = DonationCampaign.objects.filter(status='completed').order_by('-end_date')
        serializer = self.get_serializer(completed_campaigns, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='donations')
    def list_donations(self, request, pk=None):
        campaign = self.get_object()
        donations = campaign.donations.filter(is_anonymous=False).order_by('-created_at')[:20]
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

class DonationViewSet(viewsets.ModelViewSet):
    """ViewSet for creating and viewing donations"""
    queryset = Donation.objects.all().order_by('-created_at')
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DonationCreateSerializer
        return DonationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()

        # For basic testing, we'll just return the donation data
        # Payment processing will be enabled later
        return Response(
            {
                'message': 'Donation created successfully (payment processing disabled for testing)',
                'donation_id': str(donation.id),
                'payment_method': donation.payment_method
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], url_path='stats', permission_classes=[IsAuthenticated])
    def statistics(self, request):
        total_donations = Donation.objects.filter(payment_status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
        total_donors = Donation.objects.filter(payment_status='completed').values('donor_email').distinct().count()
        average_donation = Donation.objects.filter(payment_status='completed').aggregate(Avg('amount'))['amount__avg'] or 0
        
        monthly_donations = []
        today = timezone.now()
        for i in range(12):
            month_start = (today - timezone.timedelta(days=i*30)).replace(day=1)
            month_end = month_start + timezone.timedelta(days=30)
            donations_in_month = Donation.objects.filter(
                payment_status='completed',
                created_at__range=(month_start, month_end)
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            monthly_donations.append(donations_in_month)
        
        recent_donations = Donation.objects.filter(payment_status='completed').order_by('-created_at')[:10]
        
        stats_data = {
            'total_donations': total_donations,
            'total_donors': total_donors,
            'average_donation': f'{average_donation:.2f}',
            'monthly_donations': monthly_donations[::-1],
            'recent_donations': DonationSerializer(recent_donations, many=True).data
        }
        
        return Response(stats_data)

# --- PayPal Redirect Views ---

from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

class PayPalExecuteView(View):
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        donation_id = kwargs.get('donation_id')
        
        if execute_paypal_payment(payment_id, payer_id, donation_id):
            # Redirect to a success page on your frontend
            return HttpResponseRedirect(f"/payment/success?donation_id={donation_id}")
        else:
            # Redirect to a failure page
            return HttpResponseRedirect(f"/payment/failed?donation_id={donation_id}")

class PayPalCancelView(View):
    def get(self, request, *args, **kwargs):
        donation_id = kwargs.get('donation_id')
        donation = get_object_or_404(Donation, id=donation_id)
        donation.payment_status = 'cancelled'
        donation.save()
        # Redirect to a cancellation page
        return HttpResponseRedirect(f"/payment/cancelled?donation_id={donation_id}")

# --- Stripe Webhook View ---

class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        status_code = handle_stripe_webhook(payload, sig_header)
        return HttpResponse(status=status_code)
