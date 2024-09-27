Overview
The Flight Booking System is a web application that allows users to search for flights, book tickets, and manage their bookings. Built with Django REST Framework, this application offers a seamless user experience for flight management.

Features
User authentication and authorization
Flight search by departure city, destination city, and date
Ticket booking management (create, retrieve, update, delete)
Custom messages for user actions
JWT authentication for secure access

Technologies Used
Backend: Django, Django REST Framework
Database: PostgreSQL
Authentication: JSON Web Tokens (JWT)
Deployment: Hosted on AWS RDS and EC2

API Endpoints

Flight User Endpoints
GET /flight-users/: List all flight users
POST /flight-users/: Create a new flight user
GET /flight-users/{id}/: Retrieve details of a specific flight user
PUT /flight-users/{id}/: Update a flight user's information
DELETE /flight-users/{id}/: Delete a flight user
POST /flight-users/token/: Obtain JWT token for flight user authentication

Flight Endpoints
GET /air-flights/: List all available flights
POST /air-flights/: Create a new flight
GET /air-flights/{id}/: Retrieve details of a specific flight
PUT /air-flights/{id}/: Update flight information
DELETE /air-flights/{id}/: Delete a flight
GET /air-flights/search/: Search for flights based on specified criteria

Ticket Endpoints
GET /tickets/: List Flight User tickets for the authenticated user
POST /tickets/: Book a new ticket
GET /tickets/{id}/: Retrieve details of a specific ticket
PUT /tickets/{id}/: Update ticket information (e.g., change booking details)
DELETE /tickets/{id}/: Cancel a ticket booking
