from rest_framework import serializers
from .models import Show, TypeTicket, Ticket, Galery

class GalerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galery
        fields = ['id', 'photo']

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id','title', 'description', 'photo', 'start_at', 'end_at', 'places']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['row', 'place']


class TypeTicketSerializer(serializers.ModelSerializer):
    capacity = serializers.ReadOnlyField()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = TypeTicket
        fields = ['id', 'type', 'price', 'rows', 'seats_in_rows', 'capacity', 'seats']

    def get_seats(self, obj):
        tickets = Ticket.objects.filter(type=obj)
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
            seats.append(row_places)
        return seats


class ShowSerializer(serializers.ModelSerializer):
    types = TypeTicketSerializer(many=True, read_only=True)

    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'photo', 'start_at', 'end_at', 'types']
