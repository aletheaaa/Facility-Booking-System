from flask import Flask, request, jsonify
from flask_cors import CORS

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
# bookingLogs_URL = "http://localhost:5001/bookinglog"

payment_URL = "http://host.docker.internal:5002/payment"
# payment_URL = "http://localhost:5002/payment"

# notification_URL = "http://host.docker.internal:3000/notification"
# notification_URL = "http://localhost:3000/notification"

# coBooker accepts booking
@app.route("/coBookerAccepts", methods=["PUT"])
def getAvailableBooking():
    data = request.get_json()
    '''connecting to bookinglogs microservice'''
    # update acceptStatus in bookingLogs
    # the accountID in data is the accountID of the coBooker
    booking_result = invoke_http(bookingLogs_URL + "/coBookerAccept", method='PUT', json=data)
    if booking_result["code"] != 200:
        return jsonify({
            "code": booking_result["code"],
            "data": str(data),
            "message": booking_result["message"]
        }), booking_result["code"]

    '''connecting to payment microservice'''
    # if all of the cobookers have accepted the booking, deduct credits from coBookers and original booker
    # the amount passed from the frontend is the total amount of credits to be deducted. this amount still needs to be divided by the number of coBookers
    # deduct credits from coBooker
    bookingLog = invoke_http(bookingLogs_URL + "/" + str(data["bookingID"]), method='GET')
    if bookingLog["code"] != 200:
        return jsonify({
            "code": bookingLog["code"],
            "data": str(data),
            "message": bookingLog["message"]
        }), bookingLog["code"]

    if len(bookingLog["data"]["coBooker"]) == 0:
        return jsonify({
            "code": 404,
            "data": str(data),
            "message": "Wrong bookingID provided."
        }), 404

    # looping through the coBookers to see if all of them have accepted the booking to see if credits need to be subtracted from this coBooker
    allAccepted = True
    for coBooker in bookingLog["data"]["coBooker"]:
        if coBooker["acceptStatus"] == "False":
            allAccepted = False
            break
    if allAccepted:
        amountForEachBooker = bookingLog["data"]["price"] / (len(bookingLog["data"]["coBooker"]) + 1)
        allAccounts = [bookingLog["data"]["accountID"]]
        for coBooker in bookingLog["data"]["coBooker"]:
            allAccounts.append(coBooker["accountID"])
        paymentData = { "accountID": allAccounts, "amount": amountForEachBooker }
        order_result = invoke_http(payment_URL + "/deduct", method='POST', json=paymentData)
        if order_result["code"] != 200:
            return jsonify({
                "code": order_result["code"],
                "data": str(data),
                "message": order_result["message"]
            }), order_result["code"]

    '''connecting to notification microservice'''
    # connect to notification service to send notification to
    

    return jsonify({
            "code": 200,
            "data": str(data),
            "message": "Successfully updated booking"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

