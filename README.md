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

## Access to Front-End UI
To run the web application, run this code in the terminal, `npm run dev`.

We make use of Vue3 to render the frontend webpages. The user begins with the login page, and goes to the main page to make booking or go to the bookings page to confirm co-booker status. 

All our frontend webpages can also be accessed via these links:
1. Login :              http://127.0.0.1:5173/
2. Landing page:        http://127.0.0.1:5173/main
3. Make Booking page:   http://127.0.0.1:5173/book
4. Account page:        http://127.0.0.1:5173/account
5. Admin access page: : http://127.0.0.1:5173/admin 


## Login Credentials
At the login page, we use a test user with the following credentials to reach the landing page which includes the 
Email: 'john.doe@example.com' | PW: 'testest'

The admin access page is accessed if the user inputs the admin credentials in the login page
Email: 'admin@admin.com' | PW: 'adminadmin'
