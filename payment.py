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


@app.route('/deduct', methods=['POST'])
def deduct():
    data = request.get_json()
    account_id = data['accountID']
    amount = data['amount']

    account = accounts.query.get(account_id)
    if account is None:
        return f"Account with ID {account_id} does not exist", 404

    if account.balance < amount:
       return "Insufficient funds", 400

    account.balance -= amount
    db.session.commit()

    return f"Successfully deducted {amount} credits from account {account_id}"

@app.route('/refund', methods=['POST'])
def refund():
    data = request.get_json()
    account_id = data['accountID']
    amount = data['amount']

    account = accounts.query.get(account_id)
    if account is None:
        return f"Account with ID {account_id} does not exist", 404

    account.balance += amount
    db.session.commit()

    return f"Successfully refunded {amount} credits to account {account_id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
