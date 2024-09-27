# Generated by Django 5.0.2 on 2024-09-27 05:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=5)),
                ('booking_status', models.CharField(choices=[('booked', 'Booked'), ('canceled', 'Canceled')], default='booked', max_length=10)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.flightuser')),
            ],
            options={
                'unique_together': {('flight', 'seat_number')},
            },
        ),
    ]