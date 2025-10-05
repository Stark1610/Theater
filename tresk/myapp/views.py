from rest_framework.viewsets import ModelViewSet
from .serializers import (
    GalerySerializer,
    ShowSerializer,
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
from rest_framework import permissions, generics

User = get_user_model()

class GaleryViewSet(ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer

class ShowViewSet(ModelViewSet):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(start_at__gte = timezone.now()).order_by("start_at")


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


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