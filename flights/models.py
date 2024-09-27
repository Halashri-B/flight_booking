from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class FlightUserManager(BaseUserManager):
    def create_user(self, phone_number,password):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            phone_number=phone_number,
            password=password
        )
        user.save(using=self._db)
        return user


class FlightUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    objects = FlightUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number','email']

    def save(self, *args, **kwargs):
        super(FlightUser, self).save(*args, **kwargs)


class Flight(models.Model):
    airline = models.CharField(max_length=50)
    flight_number = models.CharField(max_length=10, unique=True)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)


class Ticket(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
    )
    
    user = models.ForeignKey(FlightUser, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=20, null=True, blank=True)
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, default='booked')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f'Ticket {self.id} - Flight: {self.flight.flight_number} - Seat: {self.seat_number}'
