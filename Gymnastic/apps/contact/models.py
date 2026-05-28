from django.db import models


class ContactMessage(models.Model):
    """Stores submitted contact form messages."""
    name        = models.CharField(max_length=200)
    email       = models.EmailField()
    subject     = models.CharField(max_length=300, blank=True)
    message     = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read     = models.BooleanField(default=False)
    ip_address  = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"[{self.submitted_at:%Y-%m-%d}] {self.name} — {self.subject or '(no subject)'}"


class EmailRecipient(models.Model):
    """Model to store email recipients that can be managed via Django Admin."""
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['email']
        verbose_name = "Email Recipient"
        verbose_name_plural = "Email Recipients"

    def __str__(self):
        return self.email