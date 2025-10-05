from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GaleryViewSet, ShowViewSet, TicketViewSet, TicketBatchCreateView

router = DefaultRouter()
router.register(r'gallery', GaleryViewSet, basename='gallery')
router.register(r'show', ShowViewSet, basename='show')
router.register(r'shows', ShowViewSet, basename='shows')
router.register(r'tickets', TicketViewSet, basename='tickets')

urlpatterns = [
    path("", include(router.urls)),
    path("purchase/buy/", TicketBatchCreateView.as_view(), name="tickets-buy"),
]
