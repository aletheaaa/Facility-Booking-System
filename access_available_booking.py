from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

room_URL = "http://localhost:8080/rooms/getSpecificRooms"
booking_log_URL = "http://localhost:5000/bookinglog/getTaken"

@app.route("/access_available_booking", methods=['GET'])
def access_available_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            room = request.get_json()
            print("\nReceived an order in JSON:", room)

            # do the actual work
            # 1. Send order info {cart items}
            result = processAccessAvailableBooking(room)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAccessAvailableBooking(room):
# 1. get room by user specifications
# Invoke the room microservice
    print('\n-----Invoking room microservice-----')
    room_result = invoke_http(room_URL, method='GET', json=room)
    print('room_result:', room_result)

# 2. get booked rooms by roomID
    print('\n\n-----Invoking bookingLogs microservice-----')
    booking_log_result = invoke_http(booking_log_URL, method="GET", json=room_result)
    print('booking_log_result:', booking_log_result)

# Check the room result; if a failure, return error.
    code = room_result["code"]
    if code not in range(200, 300):

        # 3. Return error
        return {
            "code": 500,
            "data": {"room_result": room_result},
            "message": "Failed to fetch rooms based on user specifications."
        }

# Check the booking logs result; 
    # if a failure, return error.
    code = booking_log_result["code"]
    if code not in range(200, 300):

        # 4. Return error
        return {
            "code": 500,
            "data": {
                "room_result": room_result,
                "booking_log_result": booking_log_result
            },
            "message": "Failed to get booked rooms by room ID."
        }
# 5. Return booking details of rooms requested by user
    return {
        "code": 200,
        "data": {
            "room_result": room_result,
            "booking_log_result": booking_log_result
        }
    }
