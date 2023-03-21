from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysqlysqlconnector://root@localhost:3306/book"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BookingLog(db.Model):
    __tablename__ = 'bookinglog'
    bookingID = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, nullable=False)
    coBookerID = db.Column(db.Integer, nullable=True)
    bkgStartTime = db.Column(db.DateTime, nullable=False)
    bkgEndTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    roomId = db.Column(db.Integer, nullable=False)

    def __init__(self, bookingID, accountID, coBookerID, bkgStartTime, bkgEndTime, price, roomId):
        self.bookingID = bookingID
        self.accountID = accountID
        self.coBookerID = coBookerID
        self.bkgStartTime = bkgStartTime
        self.bkgEndTime = bkgEndTime
        self.price = price
        self.roomId = roomId
        
    def json(self):
        return {"bookingID": self.bookingID, "accountID": self.accountID, "coBookerID": self.coBookerID, "bkgStartTime": self.bkgStartTime, "bkgEndTime": self.bkgEndTime, "price": self.price, "roomId": self.roomId}
   
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

@app.route("/bookinglog/<integer:bookingID>")
def find_booking(bookingID):
    bookinglog = BookingLog.query.filter_by(bookingID=bookingID).first()
    if bookinglog:
        return jsonify(
            {
                "code": 200,
                "data": bookinglog.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Booking log is not found."
        }
    ), 404

@app.route("/bookinglog/<integer:bookingID>", methods=['POST'])
def create_booking(bookingID):
    if (BookingLog.query.filter_by(bookingID=bookingID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "booking": bookingID
                },
                "message": "Booking already exists."
            }
        ), 400


    data = request.get_json()
    bookinglog = BookingLog(bookingID, **data)
    try:
        db.session.add(bookinglog)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking": bookingID
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)