from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'submitted_at', 'is_read')
    list_filter   = ('is_read', 'submitted_at')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at', 'ip_address')
    search_fields = ('name', 'email', 'subject')
    ordering      = ('-submitted_at',)