import json
import requests
import os
from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from dateutil import parser
from models import *


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

try:
    req_obj = requests.get(
        "https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json"
    )
    transactions_list = req_obj.json()
except Exception as e:
    print(e)
    transactions_list = json.load(open("data/transactions.json"))


@app.route("/", methods=["GET"])
def start():
    return "<h3> Hello Welcome to Transactions API </h3>"


@app.route("/transactions/<date>", methods=["GET"])
def transactions_date(date):
    return_list = list()
    date_data = parser.parse(date).date()
    transactions = Transactions.query.filter_by(date=date_data).all()
    return_list = Transactions.return_json(transactions)
    return jsonify({"message": True, "data": return_list})


@app.route("/balance/<date>", methods=["GET"])
def balance_date(date):
    date_data = parser.parse(date).date()
    transactions = Transactions.query.filter_by(date=date_data).all()
    if transactions:
        remaining = Transactions.return_balance(transactions[-1].balance)
    else:
        remaining = ""

    return jsonify({"message": True, "remainingBalance": remaining})


@app.route("/details/:<id>", methods=["GET"])
def transactions_id(id):
    transactions = Transactions.query.filter_by(id=id).all()
    return_list = Transactions.return_json(transactions)
    return jsonify({"message": True, "data": return_list})


@app.route("/add", methods=["POST"])
def add_data():
    data = json.loads(request.data.decode())
    print(type(data))
    err, valid = Transactions.validate_addition(data)

    if err:
        return jsonify({"message": False, "error": err})
    else:
        transactions = Transactions.query.filter_by(account_no=data["account_no"]).all()
        balance = 0
        if data["withdraw"]:
            if transactions:
                balance = transactions[-1].balance - data["withdraw"]
                if balance < 0:
                    return jsonify(
                        {"message": False, "error": "Withdrawal Not Allowed"}
                    )
            else:
                return jsonify(
                    {"message": False, "error": "Account Not Found For Withdrawal"}
                )
        elif data["deposit"]:
            if transactions:
                balance = transactions[-1].balance + data["deposit"]
            else:
                balance = data["deposit"]

        final = Transactions(
            data["account_no"],
            data["details"],
            parser.parse(data["date"]).date(),
            data["withdraw"] if data["withdraw"] else 0,
            data["deposit"] if data["deposit"] else 0,
            balance,
        )
        db.session.add(final)
        db.session.commit()
        return jsonify({"message": True, "id": final.id})


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)))
