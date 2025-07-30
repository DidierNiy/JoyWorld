from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from ..models import EmailTemplate, EmailLog
from donations.models import Donation
from volunteers.models import VolunteerApplication

def send_templated_email(recipient_email, template_type, context, recipient_name='', reference_obj=None):
    """
    Sends an email using a pre-defined template.
    """
    try:
        template = EmailTemplate.objects.get(template_type=template_type, is_active=True)
    except EmailTemplate.DoesNotExist:
        print(f"Email template '{template_type}' not found or is inactive.")
        return

    # Render email content
    html_message = render_to_string(template.html_content, context)
    text_message = render_to_string(template.text_content, context) if template.text_content else ''
    
    try:
        send_mail(
            subject=template.subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Log the email
        log_email(recipient_email, template, 'sent', recipient_name, reference_obj)
        
    except Exception as e:
        print(f"Error sending email: {e}")
        log_email(recipient_email, template, 'failed', recipient_name, reference_obj, error_message=str(e))

def log_email(recipient_email, template, status, recipient_name='', reference_obj=None, error_message=''):
    """
    Logs the status of a sent email.
    """
    reference_type = reference_obj._meta.model_name if reference_obj else ''
    reference_id = str(reference_obj.id) if reference_obj else ''
    
    EmailLog.objects.create(
        recipient_email=recipient_email,
        recipient_name=recipient_name,
        subject=template.subject,
        template_used=template,
        status=status,
        provider='smtp', # Assuming default Django SMTP
        error_message=error_message,
        reference_type=reference_type,
        reference_id=reference_id
    )

# --- Specific Email Sending Functions ---

def send_donation_confirmation_email(donation: Donation):
    context = {
        'donor_name': donation.donor_name,
        'donation_amount': donation.amount,
        'campaign_title': donation.campaign.title,
        'donation_date': donation.created_at.strftime('%Y-%m-%d %H:%M')
    }
    send_templated_email(
        recipient_email=donation.donor_email,
        template_type='donation_confirmation',
        context=context,
        recipient_name=donation.donor_name,
        reference_obj=donation
    )

def send_volunteer_application_received_email(application: VolunteerApplication):
    context = {
        'volunteer_name': application.full_name,
        'opportunity_title': application.opportunity.title,
        'application_date': application.created_at.strftime('%Y-%m-%d')
    }
    send_templated_email(
        recipient_email=application.email,
        template_type='volunteer_application_received',
        context=context,
        recipient_name=application.full_name,
        reference_obj=application
    )

def send_volunteer_application_approved_email(application: VolunteerApplication):
    context = {
        'volunteer_name': application.full_name,
        'opportunity_title': application.opportunity.title,
        'contact_person': application.opportunity.contact_person,
        'contact_email': application.opportunity.contact_email
    }
    send_templated_email(
        recipient_email=application.email,
        template_type='volunteer_application_approved',
        context=context,
        recipient_name=application.full_name,
        reference_obj=application
    )
