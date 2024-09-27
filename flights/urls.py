from django.urls import path
from .views import *

urlpatterns = [
    path('flight-users/', FlightUserListCreateView.as_view(), name='flight-user-list-create'),
    path('flight-users/<int:pk>/', FlightUserRetrieveUpdateDestroyAPIView.as_view(), name='flight-user-detail'),
    path('flight-users/token/', JWTView.as_view(), name='flight-user-detail'),


    path('air-flights/', FlightListCreateView.as_view(), name='flight-list-create'),
    path('air-flights/<int:pk>/', FlightRetrieveUpdateDestroyView.as_view(), name='flight-detail'),
    path('air-flights/search/', FlightSearchView.as_view(), name='flight-search'),


    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
]