from flask import Flask, request, jsonify
from flask_cors import CORS

from invokes import invoke_http

import os, sys
import pika
import json

app = Flask(__name__)
CORS(app)

# bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
bookingLogs_URL = "http://localhost:5001/bookinglog"

# payment_URL = "http://host.docker.internal:5002/payment"
payment_URL = "http://localhost:5002/payment"

# room_URL = "http://host.docker.internal:8080/rooms"
# room_URL = "http://localhost:8080/rooms"

queueName = 'notification'
exchangeName = 'fbs'
routingKey = 'email.notifications'

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
            "data": data,
            "message": booking_result["message"]
        }), booking_result["code"]

    '''connecting to payment microservice'''
    # if all of the cobookers have accepted the booking, deduct credits from coBookers and original booker
    # the amount passed from the frontend is the total amount of credits to be deducted. this amount still needs to be divided by the number of coBookers
    # deduct credits from coBooker
    bookingLog = invoke_http(bookingLogs_URL + "/getBybookingID/" + str(data["bookingID"]), method='GET')
    if bookingLog["code"] != 200:
        return jsonify({
            "code": bookingLog["code"],
            "data": data,
            "message": bookingLog["message"]
        }), bookingLog["code"]
    if len(bookingLog["data"]["coBooker"]) == 0:
        return jsonify({
            "code": 404,
            "data": data,
            "message": "Wrong bookingID provided."
        }), 404

    # looping through the coBookers to see if all of them have accepted the booking to see if credits need to be subtracted from this coBooker
    allAccepted = True
    for coBooker in bookingLog["data"]["coBooker"]:
        if coBooker["acceptStatus"] == "False":
            allAccepted = False
            break
    if allAccepted:
        print(bookingLog["data"]["coBooker"])
        print(len(bookingLog["data"]["coBooker"]) + 1)
        amountForEachBooker = bookingLog["data"]["price"] / (len(bookingLog["data"]["coBooker"]) + 1)
        allAccounts = []
        for coBooker in bookingLog["data"]["coBooker"]:
            allAccounts.append(coBooker["accountID"])
        paymentData = { "accountID": allAccounts, "amount": amountForEachBooker }
        print(paymentData)
        # deducting credits from all coBooker accounts
        deduct_result = invoke_http(payment_URL + "/deduct", method='PUT', json=paymentData)
        if deduct_result["code"] != 200:
            return jsonify({
                "code": deduct_result["code"],
                "data": data,
                "message": deduct_result["message"]
            }), deduct_result["code"]
        # since the original booker has paid the full amount, if there are invalid accounts, he will not get as much as he would if there isnt any 
        # from order_result, get the number of valid accounts to calculate the amount to be refunded from the original booker
        originalBookerID = bookingLog["data"]["accountID"]
        amountToAdd = amountForEachBooker * (len(bookingLog["data"]["coBooker"]) - len(deduct_result["data"]["accountsNotFound"]) - len(deduct_result["data"]["accountsWithInsufficientFunds"]))
        add_result = invoke_http(payment_URL + "/add", method='PUT', json={"accountID": [originalBookerID], "amount": amountToAdd})
        print(add_result)
        if add_result["code"] not in range(200, 300):
            return jsonify({
                "code": add_result["code"],
                "data": data,
                "message": add_result["message"]
            }), add_result["code"]

    # emailAccounts: first index is the email of the original booker, and the other is the email of the coBooker accepting
    # emailAccounts = [] 
    # accountList = [bookingLog['data']['accountID'], data['accountID']]
    # print(accountList)
    # for i in accountList:
    #     account = invoke_http(payment_URL + "/" + str(i), method='GET')
    #     print(account)
    #     if account["code"] in range(200, 300):
    #         emailAccounts.append(account['data']['email'])

    # '''connecting to room microservice'''
    # # get the roomName from roomID
    # room_result = invoke_http(room_URL + "/" + str(bookingLog["data"]["roomId"]), method='GET')
    # if room_result["code"] not in range(200, 300):
    #     return jsonify({
    #         "code": room_result["code"],
    #         "message": room_result["message"],
    #     }), room_result["code"]

    # '''connecting to notification microservice'''
    # # connect to notification service to send notification to
    # formattedStartTime = dateformatting(bookingLog["data"]["startTime"])
    # formattedEndTime = dateformatting(bookingLog["data"]["endTime"])
    # message = {
    #     "bookingID": booking_result["data"]["bookingID"], 
    #     "bookerAddress": emailAccounts[0], 
    #     "coBookerAddress": [emailAccounts[1]], 
    #     "type":"update", 
    #     "roomName": room_result["data"]["roomName"], 
    #     "startTime": formattedStartTime, 
    #     "endTime": formattedEndTime 
    # }
    # print(message)
    # brokerResult = rabbitmq(message)
    # if brokerResult["code"] not in range(200, 300):
    #     return jsonify({
    #         "code": brokerResult["code"],
    #         "message": brokerResult["data"],
    #     }), brokerResult["code"]

    return jsonify({
            "code": 200,
            "data": data,
            "message": "Successfully updated booking."
        }), 200

def rabbitmq(content):
    try: 
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal'))
        channel = connection.channel()

        # Declare the exchange and set its type to "direct"
        channel.exchange_declare(exchange='my_exchange', exchange_type='direct', durable=True)

        # Serialize the payload as a JSON string
        message = json.dumps(content)

        # Publish the message to the exchange with routing key "route.es"
        channel.basic_publish(exchange=exchangeName, routing_key=routingKey, body=message, properties=pika.BasicProperties(content_type='application/json'))

        # Close the connection
        connection.close()
        return {
            "code": 200,
            "data": "Message published successfully."
        }

    except Exception as e:
        print("Failed to send message to RabbitMQ: {}".format(str(e)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return {
            "code": 500,
            "message": "RabbitMQ error: " + ex_str
        }

def dateformatting(date):
    # formatting the time from "Thu, 6 Feb 2023 05:00:00 GMT" to "2023-01-16 04:00:00"
    dateTime = date.split(" ")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months.index(dateTime[2]) + 1
    day = dateTime[1]
    if month < 10:
        month = "0" + str(month)
    if int(day) < 10:
        day = "0" + str(day)
    return dateTime[3] + "-" + month + "-" + day + "T" + dateTime[4] + "Z"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

