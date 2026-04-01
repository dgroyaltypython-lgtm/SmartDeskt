from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Executive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

import uuid

def generate_ticket_id():
    return "CSD-" + str(uuid.uuid4())[:6].upper()

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=20, default=generate_ticket_id, unique=True)
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            last_ticket = Ticket.objects.order_by('-id').first()
            if last_ticket:
                last_id = int(last_ticket.ticket_id.split('-')[1])
                new_id = last_id + 1
            else:
                new_id = 1001

            self.ticket_id = f"CSD-{new_id}"

        super().save(*args, **kwargs)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(max_length=20, default='Open')
    priority = models.CharField(max_length=20, default='Medium')

    assigned_to = models.ForeignKey(Executive, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_id