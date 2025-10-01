from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GaleryViewSet, ShowViewSet

router = DefaultRouter()
router.register(r'galery', GaleryViewSet, basename='galery')
router.register(r'show', ShowViewSet, basename='show')
router.register(r'shows', ShowViewSet, basename='shows')

urlpatterns = [
    path('', include(router.urls))
]