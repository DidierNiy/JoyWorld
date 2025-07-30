from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ContactMessage, NewsletterSubscriber
from .serializers import (
    ContactMessageSerializer, ContactMessageCreateSerializer,
    NewsletterSubscriberSerializer, NewsletterSubscribeSerializer,
    NewsletterUnsubscribeSerializer
)

class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Contact Messages"""
    queryset = ContactMessage.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class NewsletterViewSet(viewsets.ModelViewSet):
    """ViewSet for Newsletter Subscriptions"""
    queryset = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NewsletterSubscribeSerializer
        elif self.action == 'unsubscribe':
            return NewsletterUnsubscribeSerializer
        return NewsletterSubscriberSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'unsubscribe']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        """Unsubscribe from newsletter using token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        try:
            subscriber = NewsletterSubscriber.objects.get(unsubscribe_token=token)
            subscriber.status = 'unsubscribed'
            subscriber.save()
            return Response({'message': 'Successfully unsubscribed'})
        except NewsletterSubscriber.DoesNotExist:
            return Response(
                {'error': 'Invalid unsubscribe token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
