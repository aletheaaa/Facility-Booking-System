import json
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

room_URL = "http://host.docker.internal:8080/rooms"
# room_URL = "http://localhost:8080/rooms"

# admin cancels booking
@app.route("/cancelBooking", methods=["DELETE"])
def getAvailableBooking():
    data = request.get_json()
    '''connecting to bookinglogs microservice'''
    # delete bookinglog table & coBooker table
    booking_deleted = invoke_http(bookingLogs_URL, method='DELETE', json=data)
    if booking_deleted["code"] not in range(200, 300):
        return jsonify({
            "code": booking_deleted["code"],
            "data": data,
            "message": booking_deleted["message"]
        }), booking_deleted["code"]
    # print(booking_deleted)

    '''connecting to payment microservice'''
    # refund credits to original booker and coBooker
    # get a list of accountIDs of coBookers & original booker to refund credits
    # check if all coBooker have paid before refunding to them. Else, only refund original coBooker
    accountsToRefund = [booking_deleted['data']['booking']['accountID']]
    temp = []
    for cobooker in booking_deleted['data']['booking']['coBooker']:
        if cobooker['acceptStatus'] == 'True':
            temp.append(cobooker['accountID'])
    if len(temp) == len(booking_deleted['data']['booking']['coBooker']):
        accountsToRefund.extend(temp)
    paymentInput = json.dumps({"accountID": accountsToRefund, "amount": (booking_deleted['data']['booking']['price'] / len(accountsToRefund))})
    payment_result = invoke_http(payment_URL + "/add", method='PUT', json=paymentInput)
    # print(payment_result)
    if payment_result["code"] not in range(200, 300):
        return jsonify({
            "code": payment_result["code"],
            "data": data,
            "message": payment_result["message"]
        }), payment_result["code"]


    '''connecting to room microservice'''
    # call on room microservice to get the specification of the room from the roomID
    roomResult = invoke_http(room_URL + "/" + str(booking_deleted['data']['booking']['roomId']), method='GET')
    # print(roomResult)

    '''connecting to notification microservice'''
    # embed information of user specification of cancelled booking into notification


    return jsonify({
        "code": 200,
        "data": roomResult,
        "message": "Booking successfully cancelled."
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

