from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryViewSet, ShowsViewSet, EventsViewSet, RegisterViewsSet, LoginViewSet, LogoutViewSet, OrderCreateView, OrderUserView

router = DefaultRouter()
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'shows', ShowsViewSet, basename='shows')
router.register(r'events', EventsViewSet, basename='events')
router.register(r'myorders', OrderUserView, basename='myorders')


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterViewsSet.as_view(), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("orders/", OrderCreateView.as_view(), name="order-create")
]
