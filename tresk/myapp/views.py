from rest_framework.viewsets import ModelViewSet
from .serializers import (
    GalerySerializer,
    ShowSerializer,
    ShowsSerializer,
    TicketSerializer,
    TicketListSerializer,
    RegisterUserSerializer
)
from .models import Galery, Show, Ticket
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, views
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class GaleryViewSet(ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer

class ShowViewSet(ModelViewSet):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(start_at__gte = timezone.now()).order_by("start_at")


class ShowsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowsSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketBatchCreateView(APIView):
    """
    POST /api/tickets/buy/
    {
      "tickets": [
        {"type_id": 1, "row": 1, "place": 1},
        {"type_id": 1, "row": 1, "place": 2}
      ]
    }
    """

    def post(self, request):
        serializer = TicketListSerializer(data=request.data.get("tickets", []))
        serializer.is_valid(raise_exception=True)
        tickets = serializer.save()
        return Response({"created": len(tickets)}, status=status.HTTP_201_CREATED)


class RegisterViewsSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

class LoginViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"errors":"Почта или пароль не введены!"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"errors": "Пользователь не найден!"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user.username, password=password)
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":{"id":user.id, "first_name":user.first_name, "last_name":user.last_name, "email":user.email}}, status=status.HTTP_200_OK)

class LogoutViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)