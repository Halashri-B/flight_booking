from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from datetime import datetime
from .models import *
from .serializers import *
from .backends import *


class FlightUserListCreateView(generics.ListCreateAPIView):
    queryset = FlightUser.objects.all()
    serializer_class = FlightUserSerializer

class FlightUserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlightUser.objects.all()
    serializer_class = FlightUserSerializer

class JWTView(generics.CreateAPIView):
    permission_classes = []

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        password = request.data.get('password')

        if not phone_number and not email:
            return Response({'error': 'Provide either phone_number or email.'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'error': 'Provide password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        if phone_number:
            user = FlightUser.objects.filter(phone_number=phone_number).first()
        elif email:
            user = FlightUser.objects.filter(email=email).first()

        if not user:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if not password == user.password:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'refresh_token': refresh_token,
            'access_token': access_token
        }, status=status.HTTP_200_OK)



class FlightListCreateView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        departure_city = self.request.query_params.get('departure_city', None)
        destination_city = self.request.query_params.get('destination_city', None)
        departure_date = self.request.query_params.get('departure_date', None)

        if departure_city:
            queryset = queryset.filter(departure_city__iexact=departure_city)
        if destination_city:
            queryset = queryset.filter(destination_city__iexact=destination_city)
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
                queryset = queryset.filter(departure_time__date=departure_date)
            except ValueError:
                return queryset.none()

        return queryset

class FlightRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightSearchView(generics.ListAPIView):
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        departure_city = self.request.query_params.get('departure_city', None)
        destination_city = self.request.query_params.get('destination_city', None)
        departure_date = self.request.query_params.get('departure_date', None)

        if departure_city:
            queryset = queryset.filter(departure_city__iexact=departure_city)
        if destination_city:
            queryset = queryset.filter(destination_city__iexact=destination_city)
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
                queryset = queryset.filter(departure_time__date=departure_date)
            except ValueError:
                return queryset.none()

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"message": "No flights found matching your criteria."}, status=status.HTTP_404_NOT_FOUND)



class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [FlightUserJWTAuthentication]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('User is not authenticated')
        return Ticket.objects.filter(user=self.request.user)


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [FlightUserJWTAuthentication]

    def perform_destroy(self, instance):
        instance.booking_status = 'canceled'
        instance.seat_number = "Cancelled"
        instance.save()

    def delete(self, request, *args, **kwargs):
        # Perform the destroy operation
        instance = self.get_object()
        self.perform_destroy(instance)

        # Return a custom response message after deletion
        return Response(
            {"message": "Ticket canceled successfully."},
            status=status.HTTP_200_OK
        )

