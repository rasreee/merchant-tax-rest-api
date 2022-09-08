import mysql.connector
from flask import Flask, jsonify, request

DB_HOST = "34.125.155.239"
DB_NAME = "transactions"
DB_USER = "root"
DB_PASS = "*eTym2vpR6z4"

PORT = 5000

app = Flask(__name__)

def create_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route("/")
def get_health():
    return {
        "success": True
    }

@app.route("/transaction-count")
def get_transaction_count():
    with create_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("select count(*) as transaction_count from transactions")
            transaction_count = cursor.fetchone()["transaction_count"]
            return {
                "transaction_count": transaction_count
            }

@app.route("/generate-schedule-c", methods=["POST"])
def generate_schedule_c():
    request_data = request.get_json()
    transactions = request_data["transactions"]
    multipliers = request_data["multipliers"]

    category_totals = {}

    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]
        if (category not in category_totals):
            category_totals[category] = amount
        else:
            prev_total = category_totals[category]
            category_totals[category] = prev_total + amount

    for category in multipliers:
        if (category not in category_totals):
            break
        multiplier = multipliers[category]
        prev_total = category_totals[category]
        category_totals[category] =  prev_total * multiplier

    print("result: ", category_totals)

    return category_totals

@app.route("/merchant-summary")
def get_merchant_summary():
    print("get_merchant_summary")
    with create_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("select merchant, sum(amount) from transactions group by merchant")
            result = cursor.fetchall()
            
            merchant_summary = {}
            for entry in result:
                merchant = entry["merchant"]
                amount = entry['sum(amount)']
                real_amount = float(amount)
                merchant_summary[merchant] = real_amount
            
            print("merchant_summary: ", merchant_summary)
            return merchant_summary

@app.route("/transactions")
def get_transactions_between_dates():
    request_data = jsonify(request.query_string)
    # print('get_transactions_between_dates: ', {"start_date": start_date, "end_date": end_date})
    print('get_transactions_between_dates: ', request_data)
    return {}

if __name__ == "__main__":
    app.run(port=PORT)
