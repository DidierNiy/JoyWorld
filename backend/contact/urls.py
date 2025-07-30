from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, NewsletterViewSet

router = DefaultRouter()
router.register(r'messages', ContactMessageViewSet)
router.register(r'newsletter', NewsletterViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
