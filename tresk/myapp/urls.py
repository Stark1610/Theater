from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GaleryViewSet, ShowsViewSet, ShowViewSet, TicketViewSet, TicketBatchCreateView, RegisterViewsSet, LoginViewSet, LogoutViewSet, OrderCreateView, OrderUserView

router = DefaultRouter()
router.register(r'gallery', GaleryViewSet, basename='gallery')
router.register(r'events', ShowViewSet, basename='events')
router.register(r'shows', ShowsViewSet, basename='shows')
router.register(r'tickets', TicketViewSet, basename='tickets')
router.register(r'myorders', OrderUserView, basename='myorders')


urlpatterns = [
    path("", include(router.urls)),
    path("purchase/buy/", TicketBatchCreateView.as_view(), name="tickets-buy"),
    path("register/", RegisterViewsSet.as_view({'post': 'create'}), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("orders/", OrderCreateView.as_view(), name="order-create")
]
