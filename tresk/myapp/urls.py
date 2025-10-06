from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GaleryViewSet, ShowsViewSet, ShowViewSet, TicketViewSet, TicketBatchCreateView,RegisterViewsSet

router = DefaultRouter()
router.register(r'gallery', GaleryViewSet, basename='gallery')
router.register(r'events', ShowViewSet, basename='events')
router.register(r'shows', ShowsViewSet, basename='shows')
router.register(r'tickets', TicketViewSet, basename='tickets')

urlpatterns = [
    path("", include(router.urls)),
    path("purchase/buy/", TicketBatchCreateView.as_view(), name="tickets-buy"),
    path("register/", RegisterViewsSet.as_view({'post': 'create'}), name="register")
]
