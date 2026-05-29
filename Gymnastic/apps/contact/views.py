from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage, EmailRecipient
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings

class ContactFormView(APIView):
    """POST /api/contact/ — Accepts and saves contact form submissions."""
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            # Save the contact message
            contact_message = serializer.save(
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Send email to the owner
            subject = f"New Contact Message from {contact_message.name}"
            message = f"""
You have received a new contact message from Bendre's Gymnastics Club website:
            
Name: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject or 'No subject'}
Message: {contact_message.message}
Submitted at: {contact_message.submitted_at}
IP Address: {contact_message.ip_address or 'Not available'}
            
This message was automatically sent from the contact form on Bendre's Gymnastics Club website.
            """
            from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'subhabratabarik7@gmail.com'
            # Get active email recipients from the database
            recipient_list = list(EmailRecipient.objects.filter(is_active=True).values_list('email', flat=True))
            
            # If no recipients are configured, fall back to default
            if not recipient_list:
                recipient_list = ['bariksubhabrata945gmail.com', ' tejasbendre92@gmail.com']
            
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                # Log the error but don't fail the form submission
                print(f"Failed to send email: {e}")
            
            return Response(
                {'success': True, 'message': 'Your message has been sent!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)