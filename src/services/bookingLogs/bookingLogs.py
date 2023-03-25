from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime, date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://is213@localhost:3306/bookinglogs"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BookingLog(db.Model):
    __tablename__ = 'bookinglogs'
    bookingID = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    roomID = db.Column(db.Integer, nullable=False)

    # relationship: orders
    coBookers = relationship(
        'CoBooker',
        cascade='save-update, merge, delete'
    )

    def json(self):
        dto = {
            "bookingID": self.bookingID, 
            "accountID": self.accountID, 
            "startTime": self.startTime, 
            "endTime": self.endTime, 
            "price": self.price, 
            "roomId": self.roomID
        }

        dto['coBooker'] = []
        for oi in self.coBooker:
            dto['coBooker'].append(oi.json())

        return dto
   
class CoBooker(db.Model):
    __tablename__ = 'coBooker'
    accountID = db.Column(db.Integer, primary_key=True)
    bookingID = db.Column(db.ForeignKey(
        'bookinglogs.bookingID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    paidStatus = db.Column(db.String(36), nullable=False)

    bookingLog = db.relationship(
        'BookingLog', primaryjoin='CoBooker.bookingID == BookingLog.bookingID', backref='coBooker')

    def json(self):
        return {'accountID': self.accountID, 'bookingID': self.bookingID, 'paidStatus': self.paidStatus}

# get all bookings
@app.route("/bookinglog")
def get_all():
    bookingloglist = BookingLog.query.all()
    if len(bookingloglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bookinglogs": [bookinglog.json() for bookinglog in bookingloglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings at this time."
        }
    ), 404


# get all booking by accountID
@app.route("/bookinglog/<int:accountID>")
def find_by_accountID(accountID):
    bookingloglist = BookingLog.query.filter_by(accountID=accountID).all()
    if len(bookingloglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bookinglogs": [bookinglog.json() for bookinglog in bookingloglist]
                }
            }
        )   
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings at this time."
        }
    ), 404


# get all the bookings for the selected fields to get the available rooms
@app.route("/bookinglog/getTaken", methods=['GET'])
def find_booking():
    data = request.get_json()
    if (data == None or len(data["roomID"]) == 0):
        return jsonify({
            "code": 400,
            "message": "Provide a roomID."
        })

    final = []
    for i in data["roomID"]:
        bookinglog = BookingLog.query.filter_by(roomID=i).all()
        final.extend(bookinglog)
    if len(final) != 0:
        return jsonify(
            {
                "code": 200,
                "data": [bookinglog.json() for bookinglog in final]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No booking log found."
        }
    ), 404

# create a new booking
@app.route("/bookinglog/", methods=['POST'])
def create_booking():
    # checking if all the fields are filled by the user
    data = request.get_json()
    if ((data["accountID"] == None) or (data["startTime"] == None) or (data["endTime"] == None) or (data["price"] == None) or (data["roomID"] == None)):
        return jsonify({
            "code": 400,
            "message": "Provide all the fields."
        })
    
    dataWithoutCoBooker = data.copy()
    dataWithoutCoBooker.pop("coBooker", None)

    # assume that data is valid since users can only click on valid time slots
    bookinglog = BookingLog(**dataWithoutCoBooker)

    # checking if coBooker field was filled
    try:
        data["coBooker"]
        for i in range(len(data["coBooker"])):
            bookinglog.coBooker.append(CoBooker(
                accountID=data["coBooker"][i], paidStatus="False"))
    except:
        None

    try:
        db.session.add(bookinglog)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking": bookinglog
                },
                "message": "An error occurred creating the booking."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": bookinglog.json()
        }
    ), 201

# delete booking by roomID & timeslot
@app.route("/bookinglog", methods=['DELETE'])
def delete_booking():
    data = request.get_json()
    
    # checking if the relevant fields are filled
    if ((data["startTime"] == None) or (data["endTime"] == None) or (data["roomID"] == None)):
        return jsonify({
            "code": 400,
            "message": "Provide all the fields: startTime, endTime, roomID."
        })
    
    # filter by roomID & timeslot
    bookinglog = BookingLog.query.filter_by(roomID=data["roomID"], startTime=data["startTime"], endTime=data["endTime"]).first()
    if bookinglog:

        # !!!!!!!!!!!!! find out if coBooker table is empty
        
        db.session.delete(bookinglog)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "booking": bookinglog.json()
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)