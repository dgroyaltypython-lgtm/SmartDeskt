from django.core.management.base import BaseCommand
import imaplib
import email
import re

from django.conf import settings
from tickets.models import Customer, Ticket, Executive
from tickets.utils import send_ticket_confirmation, notify_executive


class Command(BaseCommand):
    help = 'Fetch emails and create tickets'

    def handle(self, *args, **kwargs):
        self.stdout.write("Connecting to Gmail...")

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')

        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            subject = msg["subject"]
            raw_from = msg["from"]

            # ✅ Extract clean email
            email_match = re.search(r'<(.+?)>', raw_from)
            from_email = email_match.group(1) if email_match else raw_from

            # ✅ Extract body
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')

            # ✅ Create or get customer
            customer, created = Customer.objects.get_or_create(email=from_email)

            # ✅ Assign executive (simple logic)
            executive = Executive.objects.first()

            # ✅ Create ticket
            ticket = Ticket.objects.create(
                customer=customer,
                subject=subject,
                description=body,
                assigned_to=executive
            )

            # ✅ Send confirmation to customer
            print("Sending confirmation to:", customer.email)
            
            send_ticket_confirmation(customer.email, ticket.ticket_id)
            

            # ✅ Notify executive
            if executive:
                notify_executive(executive.email, ticket)

            self.stdout.write(self.style.SUCCESS(f"Ticket created: {ticket.ticket_id}"))