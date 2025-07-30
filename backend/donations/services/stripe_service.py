import stripe
from django.conf import settings
from ..models import Donation, DonationCampaign

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_payment_intent(donation: Donation):
    """
    Creates a Stripe PaymentIntent for a donation.
    Returns the client_secret needed for frontend confirmation.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(donation.amount * 100),  # Amount in cents
            currency='usd',
            description=f'Donation to {donation.campaign.title}',
            metadata={
                'donation_id': str(donation.id),
                'campaign_id': str(donation.campaign.id),
                'donor_email': donation.donor_email,
            },
            automatic_payment_methods={'enabled': True},
        )
        
        donation.payment_intent_id = intent.id
        donation.save()
        
        return intent.client_secret
    except Exception as e:
        # Handle Stripe errors
        print(f"Error creating Stripe PaymentIntent: {e}")
        return None

def handle_stripe_webhook(payload, sig_header):
    """
    Handles incoming Stripe webhooks to update donation status.
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 400

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        donation_id = payment_intent.metadata.get('donation_id')
        
        try:
            donation = Donation.objects.get(id=donation_id)
            donation.payment_status = 'completed'
            donation.transaction_id = payment_intent.latest_charge
            donation.save()
            
            # Update campaign raised amount
            campaign = donation.campaign
            campaign.raised_amount += donation.amount
            campaign.save()
            
            # Trigger notification/receipt email
            from contact.services.email_service import send_donation_confirmation_email
            send_donation_confirmation_email(donation)
            
        except Donation.DoesNotExist:
            # Handle case where donation is not found
            pass
    
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        donation_id = payment_intent.metadata.get('donation_id')
        
        try:
            donation = Donation.objects.get(id=donation_id)
            donation.payment_status = 'failed'
            donation.save()
        except Donation.DoesNotExist:
            pass

    return 200
