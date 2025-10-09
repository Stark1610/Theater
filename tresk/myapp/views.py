from rest_framework.viewsets import ModelViewSet 
from .serializers import (GalerySerializer, ShowsSerializer, EventsSerializer, RegisterUserSerializer, OrderCreateSerializer, OrderListSerializer)
from .models import Gallery, Show, Ticket, Order
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions, generics, views
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Prefetch

User = get_user_model()

class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GalerySerializer


class ShowsViewSet(ModelViewSet):
    serializer_class = ShowsSerializer

    def get_queryset(self):
        return Show.objects.filter(start_at__gte = timezone.now()).order_by("start_at")


class EventsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Show.objects.all()
    serializer_class = EventsSerializer


class RegisterViewsSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token = Token.objects.create(user=user)
            response = Response(status=status.HTTP_201_CREATED)
            response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                samesite="Lax",
                secure=False
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"errors": "Пользователь не найден!"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({"errors":"Почта или пароль не введены!"}, status=status.HTTP_400_BAD_REQUEST)
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        login(request, user)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
                key="auth_token",
                value=token.key,
                httponly=True,
                samesite="Lax",
                secure=False
            )
        return response


class LogoutViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("auth_token")
        return response


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.none()

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(status=status.HTTP_201_CREATED)


class OrderUserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderListSerializer
    def get_queryset(self):
        user_email = self.request.user.email
        tickets = Ticket.objects.select_related("type_ticket", "type_ticket__show")
        return Order.objects.filter(email=user_email).prefetch_related(Prefetch("tickets", queryset=tickets)).order_by("-created_at")
