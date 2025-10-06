from rest_framework import serializers
from .models import Show, TypeTicket, Ticket, Galery
from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()

class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = ['id', 'photo']

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id','title', 'description', 'photo', 'start_at', 'end_at', 'city', 'adress']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["type_ticket", "row", "place"]


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


class ShowsSerializer(serializers.ModelSerializer):
    types = TypeTicketSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'photo', 'start_at', 'end_at', 'types']


class TicketItemSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ticket
        fields = ["type_id", "row", "place"]

    def validate(self, data):
        tt = TypeTicket.objects.filter(id=data["type_id"]).first()
        if not tt:
            raise serializers.ValidationError({"type_id": "Такого типа билета нет"})
        if data["row"] > tt.rows:
            raise serializers.ValidationError({"row": f"Максимальный ряд {tt.rows}"})
        if data["place"] > tt.seats_in_rows:
            raise serializers.ValidationError(
                {"place": f"Максимальное место {tt.seats_in_rows}"}
            )
        data["type"] = tt
        return data


class TicketListSerializer(serializers.ListSerializer):
    child = TicketItemSerializer()

    def create(self, validated_data):
        created = []
        conflicts = []

        with transaction.atomic():
            for item in validated_data:
                item.pop("type_id", None)
                try:
                    with transaction.atomic():
                        created.append(Ticket.objects.create(**item))
                except IntegrityError:
                    conflicts.append(
                        {
                            "type": item["type"].id,
                            "row": item["row"],
                            "place": item["place"],
                            "error": "Место уже занято",
                        }
                    )

            if conflicts:
                raise serializers.ValidationError(
                    {"detail": "Некоторые места недоступны", "errors": conflicts}
                )

        return created

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
        first_name = validated_date.get("first_name")
        last_name = validated_date.get("last_name")
        username = f"{first_name}_{last_name}"
        user = User(username=username, **validated_date)
        user.set_password(password)
        user.save()
        return user

