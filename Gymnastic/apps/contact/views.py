from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactFormView(APIView):
    """POST /api/contact/ — Accepts and saves contact form submissions."""
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return Response(
                {'success': True, 'message': 'Your message has been sent!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)