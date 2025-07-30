import paypalrestsdk
from django.conf import settings
from django.urls import reverse
from ..models import Donation, DonationCampaign

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_paypal_payment(donation: Donation, request):
    """
    Creates a PayPal payment and returns the approval URL.
    """
    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    reverse('paypal-execute', kwargs={'donation_id': donation.id})
                ),
                "cancel_url": request.build_absolute_uri(
                    reverse('paypal-cancel', kwargs={'donation_id': donation.id})
                )
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Donation to {donation.campaign.title}",
                        "sku": str(donation.id),
                        "price": str(donation.amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(donation.amount),
                    "currency": "USD"
                },
                "description": f"Donation for the cause: {donation.campaign.title}"
            }]
        })

        if payment.create():
            donation.paypal_order_id = payment.id
            donation.save()
            
            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href
        else:
            print(f"Error creating PayPal payment: {payment.error}")
            return None
            
    except Exception as e:
        print(f"Exception creating PayPal payment: {e}")
        return None

def execute_paypal_payment(payment_id, payer_id, donation_id):
    """
    Executes a PayPal payment after user approval.
    """
    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            donation = Donation.objects.get(id=donation_id)
            donation.payment_status = 'completed'
            donation.transaction_id = payment.transactions[0].related_resources[0].sale.id
            donation.save()

            # Update campaign raised amount
            campaign = donation.campaign
            campaign.raised_amount += donation.amount
            campaign.save()
            
            # Trigger notification/receipt email
            from contact.services.email_service import send_donation_confirmation_email
            send_donation_confirmation_email(donation)
            
            return True
        else:
            print(f"Error executing PayPal payment: {payment.error}")
            return False
            
    except Donation.DoesNotExist:
        return False
    except Exception as e:
        print(f"Exception executing PayPal payment: {e}")
        return False
