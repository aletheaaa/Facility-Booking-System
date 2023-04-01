from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://is213@localhost:3306/accounts" 
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
        return {"accountID": self.accountID, "email": self.email, "balance": self.balance}

# get all accounts
@app.route("/payment/getAllAccounts", methods=["GET"])
def get_all():
    account_list = accounts.query.all()
    if len(account_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "accounts": [account.json() for account in account_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no accounts."
        }
    ), 404

# get the credits of the account
@app.route('/payment/<int:accountID>', methods=['GET'])
def getPaymentAccount(accountID):
    account = accounts.query.filter_by(accountID=accountID).first()
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
@app.route('/payment/deduct', methods=['PUT'])
def deduct():
    print("deducting credits")
    data = request.get_json()
    account_ids = data['accountID']
    originalBookerID = data['accountID'][0]
    amount = data['amount']

    accountsNotFound = []
    accountsWithInsufficientFunds = []
    validAccounts = []
    for accountID in account_ids:
        account = accounts.query.filter_by(accountID=accountID).first()
        if account is None:
            accountsNotFound.append(accountID)
            continue
        if account.balance < amount:
            accountsWithInsufficientFunds.append(accountID)
            continue    
        validAccounts.append(accountID)
    
    # only deduct from all accounts if there are no errors. Recalculate credits to deduct if necessary. Prevent partial deduction
    # to prevent cases of insufficient funds of accounts again, total amount owed from all invalid accounts or those with insufficient funds will be added to credits deducted from original booker account
    # ^(original booker is confirmed to have sufficient funds on booking creation & payment deduction happens on booking creation)
    if len(validAccounts) == 0:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "accountID": account_ids,
                    "amount": amount,
                    "accountsNotFound": accountsNotFound,
                    "accountsWithInsufficientFunds": accountsWithInsufficientFunds
                },
                "message": "No valid accounts with insufficient funds found."
            }), 404
    elif len(validAccounts) != len(account_ids):
        costByInvalidAccounts = (len(account_ids) - len(validAccounts)) * amount
    for accountID in validAccounts:
        account = accounts.query.filter_by(accountID=accountID).first()
        if accountID == originalBookerID:
            account.balance -= (amount + costByInvalidAccounts)
        else:
            account.balance -= amount
        db.session.commit()

    return jsonify(
            {
                "code": 200,
                "data": {
                    "accountID": account_ids,
                    "amount": amount,
                    "accountsNotFound": accountsNotFound,
                    "accountsWithInsufficientFunds": accountsWithInsufficientFunds
                },
                "message": "Successfully deducted " + str(amount) + " credits from the accounts."
            }
        ), 200

# add credits
@app.route('/payment/add', methods=['PUT'])
def refund():
    data = request.get_json()
    account_ids = data['accountID']
    amount = data['amount']

    accountsNotFound = []
    accountsFound = []
    for accountID in account_ids:
        account = accounts.query.filter_by(accountID=accountID).first()
        if account is None:
            accountsNotFound.append(accountID)
            continue
        accountsFound.append(accountID)
        account.balance += amount
        db.session.commit()

    successMessage = "Successfully refunded " + str(amount) + " credits to the accounts."
    return jsonify(
            {
                "code": 200,
                "data": {
                    "accountID": accountsFound,
                    "amount": amount,
                    "accountsNotFound": accountsNotFound,
                },
                "message": successMessage
            }
        ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
