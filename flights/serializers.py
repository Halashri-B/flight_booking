from rest_framework import serializers
from .models import *
import re


class FlightUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightUser
        fields = ['id', 'name', 'phone_number', 'password', 'email', 'dob', 'country', 'state', 'gender', 'created_at']

    def validate_password(self, value):
        if (not re.search(r'[A-Z]', value) or
                not re.search(r'[a-z]', value) or
                not re.search(r'[0-9]', value) or
                not re.search(r'[@#$%^&+=]', value)):
            raise serializers.ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        return value

class TicketFlightUserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FlightUser
        fields = ['name', 'phone_number', 'email', 'country', 'state', 'gender']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'airline', 'flight_number', 'departure_city', 'destination_city', 'departure_time', 'arrival_time', 'price', 'created_at']


class TicketFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['airline', 'flight_number', 'departure_city', 'destination_city', 'departure_time', 'arrival_time', 'price']


class TicketSerializer(serializers.ModelSerializer):
    user_data = TicketFlightUserSerilizer(source='user', read_only=True)
    flight_data = TicketFlightSerializer(source='flight', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'flight', 'user_data', 'flight_data', 'seat_number', 'booking_status', 'booked_at']
        read_only_fields = ['user']