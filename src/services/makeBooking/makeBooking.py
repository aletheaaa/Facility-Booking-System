#import sys
#sys.path.append('../utils')  # Add parent directory to Python path

from invokes import invoke_http  # Import the function from the module

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import pika
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

bookingLogs_URL = "http://host.docker.internal:5001/bookinglog"
# bookingLogs_URL = "http://localhost:5001/bookinglog"

payment_URL = "http://host.docker.internal:5002/payment/deduct"
# payment_URL = "http://localhost:5002/payment/deduct"

accessTakenURL = "http://host.docker.internal:5004/accessTakenBooking"
# accessTakenURL = "http://localhost:5004/accessTakenBooking"

queueName = 'notification'
exchangeName = 'fbs'
routingKey = 'email.notifications'

@app.route("/makeBooking", methods=['POST'])
def makeBooking():
    if request.is_json:
        try:
            booking = request.get_json()
            payment_json, bookingLog_json = convert_json(booking)            
            
            '''calling on bookinglogs microservice'''
            # check if the booking log has been created before (same timeslot & room)
            dateChosen = booking["startTime"].split(" ")[0]
            roomsJson = json.dumps({"roomID": [booking["roomID"]], "roomType":booking["roomType"], "location": booking["location"], "dateChosen": dateChosen})
            print("this is roomsJson")
            print(roomsJson)
            bookingLogResult = invoke_http(bookingLogs_URL + "/getTaken", method='GET', json=roomsJson)
            # check if bookingLogResult has a result with the exact same timeslot
            if bookingLogResult["code"] == 200:
                for bookingLog in bookingLogResult["data"]:
                    # check if it is inbetween the timeslot
                    bookedStartTime = getDateObject(bookingLog["startTime"])
                    bookedEndTime = getDateObject(bookingLog["endTime"])

                    # 2023-01-16 04:00:00
                    bookingStartTimeList = booking["startTime"].split(" ")
                    dateList = bookingStartTimeList[0].split("-")
                    timeList = bookingStartTimeList[1].split(":")
                    bookingStartTime = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]), int(timeList[0]), int(timeList[1]), int(timeList[2]))
                    
                    # roomID & timeslot taken: 
                    # call on accessTakenBooking microservice to get a list of roomIDs with available timeslots
                    if bookedStartTime <=  bookingStartTime <= bookedEndTime:
                        print("i came here")
                        print(bookedStartTime)
                        print("this is bookingStartTime")
                        print(bookingStartTime)
                        print(bookedEndTime)
                        accessTakenBookingResult = invoke_http(accessTakenURL, method='POST', json=roomsJson)
                        print(accessTakenBookingResult)
                        if accessTakenBookingResult["code"] in range (200, 300):
                            return jsonify({
                                "code": 400,
                                "data": accessTakenBookingResult['data']['data'],
                                "message": "This timeslot is not available. Data sent are the taken rooms at the timeslot previously chosen."
                            }), 400
                        return jsonify({
                            "code": 404,
                            "data": accessTakenBookingResult,
                            "message": "Did not successfully get the taken rooms."
                        }), 404

            # creating a booking log
            print("this is bookingLog_json")
            booking_logs_response = invoke_http(bookingLogs_URL, method='POST', json=bookingLog_json)
            if booking_logs_response["code"] not in range(200, 300):
                return jsonify({
                    "code": booking_logs_response["code"],
                    "data": booking,
                    "message": booking_logs_response["message"]
                }), booking_logs_response["code"]

            '''calling on payment microservice'''
            # deduct credits from the original booker. Only upon all coBookers accepting (if any), then the original booker will be charged will be refunded
            payment_response = invoke_http(payment_URL, method='PUT', json=payment_json)
            if payment_response["code"] not in range(200, 300):
                return jsonify({
                    "code": payment_response["code"],
                    "data": booking,
                    "message": payment_response["message"]
                }), payment_response["code"]
            
            # booking["startTime"] is 2023-01-16 04:00:00
            formattedStartTime = booking["startTime"].replace(" ", "T") + "Z"
            formattedEndTime = booking["startTime"].replace(" ", "T") + "Z"
            message = {
                "bookingID": booking_logs_response["data"]["bookingID"], 
                "bookerAddress": booking["accountEmail"], 
                "coBookerAddress": booking["coBookerEmails"], 
                "type":"create", 
                "roomName": booking["roomName"], 
                "startTime": formattedStartTime, 
                "endTime": formattedEndTime 
            }
            print("this is message")
            print(message)
            brokerResult = rabbitmq(message)
            if brokerResult["code"] not in range(200, 300):
                return jsonify({
                    "code": brokerResult["code"],
                    "message": brokerResult["data"],
                }), brokerResult["code"]
            return jsonify({
                "code":200,
                "data": {
                    "bookingLogs":booking_logs_response,
                    "payment":payment_response,
                    "messageBroker":brokerResult
                }
            }), 200   
          
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "makeBooking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

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

def convert_json(data):
    accountID = data["accountID"]
    accountEmail = data["accountEmail"]
    # bookingID = data["bookingID"]
    # bookerAddress = data["bookerAddress"]
    # coBookerAddress = data["coBookerAddress"]
    # type = data["type"]
    startTime = data["startTime"]
    endTime = data["endTime"]
    # roomName = data["roomName"]
    # date = data["date"]
    price = data["price"]
    roomID = data["roomID"]
    coBookerIDs = data["coBookerIDs"]
    coBookerEmails = data["coBookerEmails"]

    #changing time from YYYY-MM-DD 04:00:00 to 1100 - 1200 in notification
    # starthour = startTime.split(" ")[1]
    # endhour = endTime.split(" ")[1]
    # time = starthour[:2] + "00 - " + endhour[:2] + "00"

    # notification_json = { "bookerAddress": bookerAddress, 
    #                 "coBookerAddress": coBookerAddress, 
    #                 "type": type, 
    #                 "bookingID": bookingID, 
    #                 "time": time, 
    #                 "roomName": roomName, 
    #                 "date": date}

    payment_json = {
        'accountID': [accountID], 
        "amount": price,
    }

    bookingLog_json = {
        'accountID': accountID, 
        "startTime": startTime,
        "endTime": endTime,
        "price": price,
        "roomID": roomID,
        "coBooker": coBookerIDs
    }

    return payment_json, bookingLog_json

def getDateObject(date):
    # date has to be in this format: Thu, 16 Feb 2023 05:00:00 GMT
    bookingLogStartList = date.split(" ")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = bookingLogStartList[3]
    month = months.index(bookingLogStartList[2])+1
    day = bookingLogStartList[1]
    hour = bookingLogStartList[4].split(":")[0]
    minute = bookingLogStartList[4].split(":")[1]
    second = bookingLogStartList[4].split(":")[2]
    dateObject = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return dateObject


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for make booking...")
    app.run(host="0.0.0.0", port=5006, debug=True)