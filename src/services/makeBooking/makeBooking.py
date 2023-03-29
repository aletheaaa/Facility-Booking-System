#import sys
#sys.path.append('../utils')  # Add parent directory to Python path

from invokes import invoke_http  # Import the function from the module

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
import pika
import json

app = Flask(__name__)
CORS(app)

booking_logs_url = "http://localhost:5001/bookinglog"
payment_url = "http://localhost:5002/payment/deduct"

queueName = 'notification'
exchangeName = 'fbs'
routingKey = 'email.notifications'

@app.route("/makeBooking", methods=['POST'])
def makeBooking():
    if request.is_json:
        try:
            booking = request.get_json()
            payment_json, bookingLog_json, notification_json = convert_json(booking)            
            
            booking_logs_response = invoke_http(booking_logs_url, method='POST', json=bookingLog_json)
            # Check if the booking logs microservice was successful
            

            # Call the payment microservice
            payment_response = invoke_http(payment_url, method='POST', json=payment_json)

            print("This is the content:",booking_logs_response)


            if (booking_logs_response["code"] == 201 and payment_response["code"] == 200):
                brokerResult = rabbitmq(notification_json)
                return jsonify({
                "code":200,
                "data": {"bookingLogs":booking_logs_response,"payment":payment_response,"messageBroker":brokerResult},
            })
            return jsonify({
                "code":500,
                "data": {"bookingLogs":booking_logs_response,"payment":payment_response},
                "message":"unsuccessful"
            })
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "update.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def rabbitmq(content):
    try: 
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
        return {
            "code": 500,
            "message": "Order creation failure sent for error handling."
        }

def convert_json(data):
    accountID = data["accountID"]
    bookingID = data["bookingID"]
    bookerAddress = data["bookerAddress"]
    coBookerAddress = data["coBookerAddress"]
    bookerID = data["bookerID"]
    coBookerID = data["coBookerID"]
    type = data["type"]
    startTime = data["startTime"]
    endTime = data["endTime"]
    roomName = data["roomName"]
    date = data["date"]
    price = data["price"]
    roomID = data["roomID"]
    coBooker = data["coBooker"]

    #changing time from YYYY-MM-DD 04:00:00 to 1100 - 1200 in notification
    starthour = startTime.split(" ")[1]
    endhour = endTime.split(" ")[1]
    time = starthour[:2] + "00 - " + endhour[:2] + "00"

    notification_json = { "bookerAddress": bookerAddress, 
                    "coBookerAddress": coBookerAddress, 
                    "bookerID": bookerID, 
                    "coBookerID": coBookerID, 
                    "type": type, 
                    "bookingID": bookingID, 
                    "time": time, 
                    "roomName": roomName, 
                    "date": date}

    payment_json = {'accountID': accountID, 
               "startTime": startTime,
               "endTime": endTime,
               "amount": price,
               "roomID": roomID,
               "coBooker": coBooker}

    bookingLog_json = {'accountID': accountID, 
               "startTime": startTime,
               "endTime": endTime,
               "price": price,
               "roomID": roomID,
                "coBooker": coBooker}

    return payment_json, bookingLog_json, notification_json

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for make booking...")
    app.run(host="0.0.0.0", port=5100, debug=True)