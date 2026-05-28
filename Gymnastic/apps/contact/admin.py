from django.contrib import admin
from .models import ContactMessage, EmailRecipient


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'submitted_at', 'is_read')
    list_filter   = ('is_read', 'submitted_at')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at', 'ip_address')


@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('email',)
    ordering = ('-created_at',)
    list_per_page = 20