import json
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

room_URL = "http://host.docker.internal:8080/rooms"

# bookingLogs_URL = "http://localhost:5001/bookinglog"
bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"

@app.route("/accessAvailableBooking", methods=['GET'])
def access_available_booking():
    if request.is_json:
        try:
            roomSpecifications = request.get_json()
            result = processAccessAvailableBooking(roomSpecifications)
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
    # user must input at least one of the two to prevent returning all rooms which requires a lot of processing
    if len(room['roomType']) == 0 and len(room['location']) == 0:
        return {
                "code": 400,
                "message": "No room type or location specified."
        }
    
    # calling room microservice to get a list of rooms based on user specifications
    roomResult = invoke_http(room_URL + "/getSpecificRooms", method='GET', json=room)
    # print(roomResult)

    # calling bookingLogs microservice to get a list of booked rooms
    roomIDs = []
    for i in roomResult["data"]:
        roomIDs.append(i["roomId"])
    roomsJson = json.dumps({"roomID": roomIDs})
    # print(roomsJson)

    if roomResult["code"] not in range(200, 300):
        return {
                "code": 500,
                "message": "Error retreiving rooms."
            }
    elif len(roomResult["data"]) == 0:
        return {
                "code": 404,
                "message": "No rooms with user specifications found."
            }

    bookingLogResult = invoke_http(bookingLogs_URL + "/getTaken", method='GET', json=roomsJson)
    print("this is bookingLogResult")
    print(bookingLogResult)

    if bookingLogResult["code"] not in range(200, 300):
        return {
            "code": 200,
            "message": "No bookings based on user's specifications found."
        }
    return {
        "code": 200,
        "data": bookingLogResult,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)