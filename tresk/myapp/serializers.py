from rest_framework import serializers
from .models import Show, TypeTicket, Ticket, Gallery, Order
from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from random import randint

User = get_user_model()


class ItemTicketSerializer(serializers.Serializer):
    type_ticket = serializers.IntegerField()
    row = serializers.IntegerField(min_value=1)
    place = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            type_tickets = TypeTicket.objects.only("id", "rows", "seats_in_rows", "price").get(
                pk=data["type_ticket"]
            )
        except TypeTicket.DoesNotExist:
            raise serializers.ValidationError({"type_ticket": "Тип билета не найден."})

        if data["row"] > type_tickets.rows:
            raise serializers.ValidationError(
                {"row": f"Ряд вне диапазона 1..{type_tickets.rows}."}
            )
        if data["place"] > type_tickets.seats_in_rows:
            raise serializers.ValidationError(
                {"place": f"Место вне диапазона 1..{type_tickets.seats_in_rows}."}
            )

        data["type_tickets"] = type_tickets
        return data


class OrderCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False, allow_blank=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    tickets = ItemTicketSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        tickets = validated_data.pop("tickets", [])
        total_price = validated_data.pop("total_price", None)
        request = self.context["request"]
        if request.user.is_authenticated:
            validated_data["email"] = request.user.email
            validated_data["full_name"] = request.user.username
        order = Order.objects.create(**validated_data)
        new_tickets = []
        for ticket in tickets:
            t = Ticket(
                order=order,
                type_ticket=ticket["type_tickets"],
                row=ticket["row"],
                place=ticket["place"],
            )
            t.clean_fields() 
            t.clean()
            new_tickets.append(t)

        try:
            Ticket.objects.bulk_create(new_tickets, batch_size=1000)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "Некоторые места уже заняты. Заказ не создан."
            })
        total = sum(i["type_tickets"].price for i in tickets)
        if total != total_price:
            raise serializers.ValidationError({"error": "Общая сумма не соответсвует!"})
        Order.objects.filter(pk=order.pk).update(total_price=total)
        order.total_price = total
        return order


class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'photo', "name"]


class ShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id','title', 'description', 'photo', 'start_at', 'end_at', 'city', 'adress']



class TypeTicketSerializer(serializers.ModelSerializer):
    capacity = serializers.ReadOnlyField()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = TypeTicket
        fields = ['id', 'type_ticket', 'price', 'rows', 'seats_in_rows', 'capacity', 'seats']

    def get_seats(self, obj):
        tickets = Ticket.objects.filter(type_ticket=obj)
        booked = {(t.row, t.place) for t in tickets}

        seats = []
        for row in range(1, obj.rows + 1):
            row_places = []
            for place in range(1, obj.seats_in_rows + 1):
                row_places.append({
                    "row": row,
                    "place": place,
                    "status": "booked" if (row, place) in booked else "free"
                })
            seats.extend(row_places)
        return seats


class EventsSerializer(serializers.ModelSerializer):
    types = TypeTicketSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'photo', 'start_at', 'end_at', 'types']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_date):
        password = validated_date.pop("password")
        first_name = validated_date.get("first_name", "first_name")
        last_name = validated_date.get("last_name", "last_name")
        username = f"{first_name}_{last_name}_{randint(1, 10000)}"
        user = User(username=username, **validated_date)
        user.set_password(password)
        user.save()
        return user

class TicketSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=5, decimal_places=2, source="type_ticket.price", read_only=True)
    type_ticket = serializers.CharField(source="type_ticket.type_ticket", read_only=True)

    class Meta:
        model = Ticket
        fields = ["type_ticket", "row", "place", "price"]

class OrderListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="tickets.first.type_ticket.show.title", read_only=True)
    description = serializers.CharField(source="tickets.first.type_ticket.show.description", read_only=True)
    photo = serializers.ImageField(source="tickets.first.type_ticket.show.photo", read_only=True)
    start_at = serializers.DateTimeField(source="tickets.first.type_ticket.show.start_at", read_only=True)
    end_at = serializers.TimeField(source="tickets.first.type_ticket.show.end_at", read_only=True)
    city = serializers.CharField(source="tickets.first.type_ticket.show.city", read_only=True)
    adress = serializers.CharField(source="tickets.first.type_ticket.show.adress", read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["full_name", "email", "title", "description", "photo", "start_at", "end_at", "city", "adress", "total_price", "tickets"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]