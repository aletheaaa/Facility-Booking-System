from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class accounts(db.Model):
    __tablename__ = 'accounts'

    accountID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False)
    balance = db.Column(db.Float(precision=2), nullable=False)
    

    def __init__(self, accountID, email, balance):
        self.accountID = accountID
        self.email = email
        self.balance = balance
        

    def json(self):
        return {"accountID": self.accountID, "email": self.email, "price": self.price, "balance": self.balance}

# get the credits of the account
@app.route('/payment/<int:accountID>', methods=['GET'])
def getPaymentAccount(accountID):
    account = accounts.query.get(accountID)
    message = "Account with ID " + str(accountID) + " does not exist" 

    if account is None:
        return jsonify({
            "code": 404,
            "message": message
        })
    return jsonify({
                "code": 200,
                "data": {
                    "accountID": accountID,
                    "accountBalance": account.balance
                }
            }
        ), 200


# deduct credits
@app.route('/payment/deduct', methods=['POST'])
def deduct():
    data = request.get_json()
    account_id = data['accountID']
    amount = data['amount']

    account = accounts.query.get(account_id)
    AccountErrorMessage = "Account with ID " + str(account_id) + " does not exist"
    if account is None:
        return jsonify({
            "code": 404,
            "data": {
                "accountID": account_id
            },
            "message": AccountErrorMessage
        }), 404
    if account.balance < amount:
        return jsonify({
            "code": 400,
            "data": {
                "accountID": account_id
            },
            "message": "Insufficient funds."
        }), 404
    account.balance -= amount
    db.session.commit()

    successMessage = "Successfully deducted " + str(amount) + " credits from account " + str(account_id)
    return jsonify(
            {
                "code": 200,
                "data": {
                    "accountID": account_id,
                    "accountBalance": account.balance
                },
                "message": successMessage
            }
        )

# add credits
@app.route('/payment/add', methods=['POST'])
def refund():
    data = request.get_json()
    account_id = data['accountID']
    amount = data['amount']

    AccountErrorMessage = "Account with ID " + str(account_id) + " does not exist"
    account = accounts.query.get(account_id)
    if account is None:
        return jsonify({
            "code": 404,
            "data": {
                "accountID": account_id
            },
            "message": AccountErrorMessage
        }), 404

    account.balance += amount
    db.session.commit()

    successMessage = "Successfully refunded " + str(amount) + " credits from account " + str(account_id)
    return jsonify(
            {
                "code": 200,
                "data": {
                    "accountID": account_id,
                    "accountBalance": account.balance
                },
                "message": successMessage
            }
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
