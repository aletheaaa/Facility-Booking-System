import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from sqlalchemy.orm import relationship
from datetime import date, datetime
from sqlalchemy import func

app = Flask(__name__)
CORS(app)

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
    acceptStatus = db.Column(db.String(36), nullable=False)

    bookingLog = db.relationship(
        'BookingLog', primaryjoin='CoBooker.bookingID == BookingLog.bookingID', backref='coBooker')

    def json(self):
        return {'accountID': self.accountID, 'bookingID': self.bookingID, 'acceptStatus': self.acceptStatus}

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
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings at this time."
        }
    ), 404

# get booking by bookingID
@app.route("/bookinglog/<int:bookingID>")
def find_by_bookingID(bookingID):
    bookinglog = BookingLog.query.filter_by(bookingID=bookingID).first()
    if bookinglog:
        return jsonify(
            {
                "code": 200,
                "data": bookinglog.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found."
        }
    ), 404

# get all booking by accountID as the original booker
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
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings at this time."
        }
    ), 404

# get all booking by accountID as a coBooker
@app.route("/bookinglog/coBooker/<int:accountID>")
def find_by_coBooker(accountID):
    bookingloglist = CoBooker.query.filter_by(accountID=accountID).all()
    # print(bookingloglist)
    if len(bookingloglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bookinglogs": [bookinglog.json() for bookinglog in bookingloglist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No booking as a coBooker found."
        }
    ), 404

# get all the bookings for the selected fields to get the available rooms
@app.route("/bookinglog/getTaken", methods=['GET'])
def find_booking():
    data = request.get_json()
    if type(data) == str:
        data = json.loads(data)
    if (len(data["roomID"]) == 0):
        return jsonify({
            "code": 400,
            "message": "Provide a roomID."
        }), 400

    final = []
    # fillter the bookinglogs by date
    date_list = data['dateChosen'].split("-")
    bookingDate = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    bookinglog = BookingLog.query.filter(func.date(BookingLog.startTime) == bookingDate).all()
    if len(bookinglog) != 0:
        # roomIDs are rooms that fit user specifications: location & roomType
        for i in data["roomID"]:
            bookinglog = list(filter(lambda x: x.roomID == i, bookinglog))
            print(bookinglog)
            final.extend(bookinglog)
        if len(final) != 0:
            return jsonify(
                {
                    "code": 200,
                    "data": [bookinglog.json() for bookinglog in final]
                }
            ), 200
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
    list_of_fields_needed = ["accountID", "startTime", "endTime", "price", "roomID", "coBooker"]
    if (not all(field in data for field in list_of_fields_needed)):
        return jsonify({
            "code": 400,
            "message": "Provide all the fields."
        }), 400
    
    dataWithoutCoBooker = data.copy()
    dataWithoutCoBooker.pop("coBooker", None)

    # assume that data is valid since users can only click on valid time slots
    bookinglog = BookingLog(**dataWithoutCoBooker)

    # checking if coBooker field was filled
    if (len(data["coBooker"]) != 0):
        for i in range(len(data["coBooker"])):
            bookinglog.coBooker.append(CoBooker(
                accountID=data["coBooker"][i], acceptStatus="False"))

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

# update booking by bookingID
@app.route("/bookinglog/coBookerAccept", methods=['PUT'])
def update_booking():
    data = request.get_json()
    fields_needed = ["accountID", "bookingID"]
    if (not all(field in data for field in fields_needed)):
        return jsonify({
            "code": 400,
            "message": "Provide all the fields."
        }), 400
    coBooker = CoBooker.query.filter_by(accountID=data["accountID"], bookingID=data["bookingID"]).first()
    if coBooker:
        if coBooker.acceptStatus == "True":
            return jsonify({
                "code": 400,
                "message": "You have already accepted this booking."
            }), 400
        coBooker.acceptStatus = "True"

        try:
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": coBooker.json()
                }
            ), 200
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating the coBooker."
                }
            ), 500
    return jsonify(
        {
            "code": 404,
            "message": "coBooker not found."
        }
    ), 404


# delete booking by roomID & timeslot
@app.route("/bookinglog", methods=['DELETE'])
def delete_booking():
    data = request.get_json()
    
    # checking if the relevant fields are filled
    if ('bookingID' not in data):
        return jsonify({
            "code": 400,
            "message": "Please provide the bookingID."
        }), 400
    
    # filter by roomID & timeslot
    bookinglog = BookingLog.query.filter_by(bookingID=data['bookingID']).first()
    if bookinglog:
        try:
            db.session.delete(bookinglog)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "booking": bookinglog.json()
                    }
                }
            ), 200
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "booking": bookinglog.json()
                    },
                    "message": "An error occurred deleting the booking."
                }
            ), 500
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)