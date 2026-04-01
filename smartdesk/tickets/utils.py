from django.core.mail import send_mail
from django.conf import settings


def send_ticket_confirmation(email, ticket_id):
    print(f"[DEBUG] Sending CUSTOMER email to: {email}")

    subject = f"Ticket Created - {ticket_id}"
    message = f"""
Thank you for contacting us.

Your ticket number is: {ticket_id}
Our team will contact you shortly.

Regards,
Support Team
"""

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        print(f"[SUCCESS] Customer email sent for ticket {ticket_id}")

    except Exception as e:
        print(f"[ERROR] Failed to send customer email: {e}")


def notify_executive(executive_email, ticket):
    print(f"[DEBUG] Sending EXECUTIVE email to: {executive_email}")

    subject = f"New Ticket Assigned - {ticket.ticket_id}"

    message = f"""
New ticket assigned to you.

Ticket ID: {ticket.ticket_id}
Customer: {ticket.customer.email}
Subject: {ticket.subject}

Please check admin panel for details.
"""

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [executive_email],
            fail_silently=False
        )
        print(f"[SUCCESS] Executive notified for ticket {ticket.ticket_id}")

    except Exception as e:
        print(f"[ERROR] Failed to notify executive: {e}")