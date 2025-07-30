from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonationCampaignViewSet, DonationViewSet,
    PayPalExecuteView, PayPalCancelView, StripeWebhookView
)

router = DefaultRouter()
router.register(r'campaigns', DonationCampaignViewSet)
router.register(r'donations', DonationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Payment gateway specific URLs
    path('paypal/execute/<uuid:donation_id>/', PayPalExecuteView.as_view(), name='paypal-execute'),
    path('paypal/cancel/<uuid:donation_id>/', PayPalCancelView.as_view(), name='paypal-cancel'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
