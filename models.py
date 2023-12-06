import locale
from datetime import date
from flask_sqlalchemy import SQLAlchemy


from babel.numbers import format_decimal

db = SQLAlchemy()


class Transactions(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_no = db.Column(db.BigInteger)
    details = db.Column(db.String(500))
    date = db.Column(db.Date, default=date.today())
    withdrawal = db.Column(db.Float)
    deposit = db.Column(db.Float)
    balance = db.Column(db.Float)

    def __init__(self, acc, details, dt, withdraw, deposit, balance):
        self.account_no = acc
        self.details = details
        self.date = dt
        self.withdrawal = withdraw
        self.deposit = deposit
        self.balance = balance

    def return_json(self):
        print(self)
        return [
            {
                "Account No": item.account_no,
                "Date": item.date.strftime("%d %b %y"),
                "Transaction Details": item.details,
                "Value Date": item.date.strftime("%d %b %y"),
                "Withdrawal AMT": format_decimal(item.withdrawal, locale="en_IN")
                if item.withdrawal
                else "",
                "Deposit AMT": format_decimal(item.deposit, locale="en_IN")
                if item.deposit
                else "",
                "Balance AMT": format_decimal(item.balance, locale="en_IN"),
            }
            for item in self
        ]

    def return_balance(self):
        return format_decimal(self, locale="en_IN")

    def validate_addition(self):
        error, data = "", []
        print(type(self))
        try:
            if type(self) == dict:
                if (
                    "account_no" not in self
                    or self["account_no"] == str
                    or self["account_no"] <= 0
                ):
                    error = "Account Number Not Correct!!!"
                    return error, data
                elif "date" not in self:
                    error = "Date Not Provided!!!"
                    return error, data
                elif "details" not in self:
                    error = "Transaction Details Not Provided!!!"
                    return error, data
                elif (
                    "withdraw" in self
                    and self["withdraw"]
                    and float(self["withdraw"]) <= 0
                ):
                    error = "Withdrawal Amount Not Correct!!!"
                    return error, data
                elif (
                    "deposit" in self
                    and self["deposit"]
                    and float(self["deposit"]) <= 0
                ):
                    error = "Deposit Amount Not Correct!!!"
                    return error, data
                return error, self
        except Exception as e:
            print(e)
            return "Error", data
        else:
            return "InCorrect Data Format", data
