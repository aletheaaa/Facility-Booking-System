import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from invokes import invoke_http

import os, sys
import pika

app = Flask(__name__)
CORS(app)

bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
# bookingLogs_URL = "http://localhost:5001/bookinglog"

payment_URL = "http://host.docker.internal:5002/payment"
# payment_URL = "http://localhost:5002/payment"

room_URL = "http://host.docker.internal:8080/rooms"
# room_URL = "http://localhost:8080/rooms"

queueName = 'notification'
exchangeName = 'fbs'
routingKey = 'email.notifications'

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
    # getting a list of emails
    accountsToNotify = []  
    accountResult = invoke_http(payment_URL + "/" + str(booking_deleted['data']['booking']['accountID']), method='GET')
    if accountResult['code'] in range(200, 300):
        accountsToNotify.append(accountResult['data']['email'])
    temp = []
    for cobooker in booking_deleted['data']['booking']['coBooker']:
        if cobooker['acceptStatus'] == 'True':
            temp.append(cobooker['accountID'])
        # getting the email of the coBookers
        coBookerAccount = invoke_http(payment_URL + "/" + str(cobooker['accountID']), method='GET')
        if coBookerAccount['code'] in range(200, 300):
            accountsToNotify.append(coBookerAccount['data']['email'])
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
    # print(accountsToNotify)  # ['msic931@gmail.com', 'alethea.toh.2021@scis.smu.edu.sg']
    locationURLFormat = roomResult['data']['location'].replace(" ", "%20")
    roomTypeURLFormat = roomResult['data']['roomType'].replace(" ", "%20")
    message = {
        "bookingID": booking_deleted['data']['booking']['bookingID'], 
        "bookerAddress": accountsToNotify[0], 
        "coBookerAddress":accountsToNotify[1:], 
        "type":"cancel", 
        "roomName": roomResult['data']['roomName'], 
        "startTime":booking_deleted['data']['booking']['startTime'],
        "endTime": booking_deleted['data']['booking']['endTime'],  
        "roomID": booking_deleted['data']['booking']['roomId'], 
        "userSpecifications": {
            "location": locationURLFormat,
            "roomType": roomTypeURLFormat,
        }
    }
    print(message)
    brokerResult = rabbitmq(message)
    print(brokerResult)  # {'code': 200, 'data': 'Message published successfully.'}
    if brokerResult["code"] not in range(200, 300):
        return jsonify({
            "code": brokerResult["code"],
            "message": brokerResult["message"],
        }), brokerResult["code"]

    return jsonify({
        "code": 200,
        "data": roomResult['data'],
        "message": "Booking successfully cancelled."
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

