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
    print("deducting credits")
    data = request.get_json()
    account_ids = data['accountID']
    amount = data['amount']
    total_amount_of_all_accounts = len(account_ids) * amount

    accountsNotFound = []
    accountsWithInsufficientFunds = []
    validAccounts = []
    for accountID in account_ids:
        account = accounts.query.get(accountID)
        if account is None:
            accountsNotFound.append(accountID)
            continue
        if account.balance < amount:
            accountsWithInsufficientFunds.append(accountID)
            continue
        validAccounts.append(accountID)
    
    # only deduct from all accounts if there are no errors. Recalculate credits to deduct if necessary. Prevent partial deduction
    message = ""
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
        amount = total_amount_of_all_accounts / len(validAccounts)
    for accountID in validAccounts:
        account = accounts.query.get(accountID)
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
@app.route('/payment/add', methods=['POST'])
def refund():
    data = request.get_json()
    account_ids = data['accountID']
    amount = data['amount']

    accountsNotFound = []
    accountsFound = []
    for accountID in account_ids:
        account = accounts.query.get(accountID)
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
