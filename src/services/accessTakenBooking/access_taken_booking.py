import json
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

room_URL = "http://host.docker.internal:8080/rooms"
# room_URL = "http://localhost:8080/rooms"

bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
# bookingLogs_URL = "http://localhost:5001/bookinglog"

@app.route("/accessTakenBooking", methods=['POST'])
def access_taken_booking():
    if request.is_json:
        try:
            roomSpecifications = request.get_json()
            result = getTakenBooking(roomSpecifications)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "accessTakenBooking.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def getTakenBooking(data):
    # user must input at least one of the two to prevent returning all rooms which requires a lot of processing
    if type(data) == str:
        data = json.loads(data)
    # checking if user has specified any room type or location or dateChosen
    if (len(data['roomType']) == 0 or len(data['location']) == 0) or 'dateChosen' not in data:
        return {
                "code": 400,
                "message": "Date must be specific. Either room type or location must also be specified."
        }
    
    # calling room microservice to get a list of rooms based on user specifications
    roomResult = invoke_http(room_URL + "/getSpecificRooms", method='GET', json=data)
    print(roomResult)

    # calling bookingLogs microservice to get a list of booked rooms
    roomIDs = []
    for i in roomResult["data"]:
        roomIDs.append(i["roomId"])
    roomsJson = json.dumps({"roomID": roomIDs, "dateChosen": data["dateChosen"]})
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
    print(bookingLogResult)
    
    if bookingLogResult["code"] not in range(200, 300):
        print("this is the error message")
        return {
            "code": 404,
            "message": "No bookings based on user's specifications found."
        }
    print("this is success mesasge")
    return {
        "code": 200,
        "data": bookingLogResult,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)