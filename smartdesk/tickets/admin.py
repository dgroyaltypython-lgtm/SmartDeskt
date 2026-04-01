from django.contrib import admin
from .models import Customer, Ticket, Executive

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'created_at']

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'customer', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['ticket_id', 'customer__email']