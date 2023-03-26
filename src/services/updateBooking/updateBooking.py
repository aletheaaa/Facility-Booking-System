import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# room_URL = "http://host.docker.internal:8080/room"


bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
# bookingLogs_URL = "http://localhost:5001/bookinglog"

payment_URL = "http://host.docker.internal:5002/payment"
# payment_URL = "http://localhost:5002/payment"

@app.route("/coBookerAccepts", methods=["GET"])
def getAvailableBooking():
    data = request.get_json()
    # update acceptStatus in bookingLogs
    booking_result = invoke_http(bookingLogs_URL + "/coBookerAccept", method='PUT', json=data)
    # print(booking_result)  # {'code': 200, 'data': {'acceptStatus': 'True', 'accountID': 2, 'bookingID': 1}}
    if booking_result["code"] != 200:
        return jsonify({
            "code": 400,
            "data": str(data),
            "message": "coBooker not found."
        }), 400
    
    # if all of the cobookers have accepted the booking, deduct credits from coBookers and original booker
    # the amount passed from the frontend is the total amount of credits to be deducted. this amount still needs to be divided by the number of coBookers
    # deduct credits from coBooker
    bookingLog = invoke_http(bookingLogs_URL + "/" + str(data["bookingID"]), method='GET')
    print(bookingLog)  # {'code': 200, 'data': {'accountID': 1, 'bookingID': 1, 'coBooker': [{'acceptStatus': 'True', 'accountID': 2, 'bookingID': 1}, {'acceptStatus': 'False', 'accountID': 3, 'bookingID': 1}], 'endTime': 'Thu, 12 Jan 2023 02:30:00 GMT', 'price': 20.0, 'roomId': 1, 'startTime': 'Thu, 12 Jan 2023 02:00:00 GMT'}}

    # looping through the coBookers to see if all of them have accepted the booking
    allAccepted = True
    print("i am here")
    for coBooker in bookingLog["data"]["coBooker"]:
        if coBooker["acceptStatus"] == "False":
            allAccepted = False
            break
    if allAccepted:
        print("pls i came here")
        amountForEachBooker = bookingLog["data"]["price"] / (len(bookingLog["data"]["coBooker"]) + 1)
        allAccounts = [bookingLog["data"]["accountID"]]
        for coBooker in bookingLog["data"]["coBooker"]:
            allAccounts.append(coBooker["accountID"])
        paymentData = { "accountID": allAccounts, "amount": amountForEachBooker }
        order_result = invoke_http(payment_URL + "/deduct", method='POST', json=paymentData)
        print(order_result)

    return jsonify({
            "code": 200,
            "data": str(data),
            "message": "Successfully updated booking"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

