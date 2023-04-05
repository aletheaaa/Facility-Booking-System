# SQL Configuration
Services that uses the SQL database will require the user to:

    1) Create a SQL account "is213"
    2) Edit the following line with their SQL port number:
        For example (for port 3306): app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://is213@localhost:3306/bookinglogs

# Facility Booking System
Our facility booking system allows students to book facilities. The microservices under our enterprise solution are BookingLogs, Payment, Room, Notification, AccessTakenBooking, CancelBooking, MakeBooking, and UpdateBooking.

## Prerequisites
Import the SQL scripts, each stored in each of the simple microservices. There are 4 SQL scripts to import: BookingLogs, Payment, Room, and Notification. Ensure that MySQL is on your local computer. 

## Running with Docker
Alternatively, you can run the entire back-end using docker in one command, `docker compose up --build`. 

## Access to Front-End 