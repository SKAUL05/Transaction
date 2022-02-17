import json
from this import d
from models import Transactions
# from app import app, db
# from dateutil import parser


# trans = json.load(open("data/transactions.json"))
# print(len(trans))

# for item in trans:
#     try:
#         w = (
#             float(item["Withdrawal AMT"].replace(",", ""))
#             if item["Withdrawal AMT"]
#             else 0.0
#         )
#         d = float(item["Deposit AMT"].replace(",", "")) if item["Deposit AMT"] else 0.0
#         b = float(item["Balance AMT"].replace(",", "")) if item["Balance AMT"] else 0.0
#         t = Transactions(
#             item["Account No"],
#             item["Transaction Details"],
#             parser.parse(item["Value Date"]).date(),
#             w,
#             d,
#             b,
#         )
#         db.session.add(t)
#         db.session.commit()
#     except Exception as e:
#         print(e)
