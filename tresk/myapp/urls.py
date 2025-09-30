from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GaleryViewSet

router = DefaultRouter()
router.register(r'galery', GaleryViewSet, basename='galery')

urlpatterns = [
    path('', include(router.urls))
]