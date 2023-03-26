from flask import Flask, flash, request, jsonify
from conn import set_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

#
# def set_connection():
#     cur, conn = None, None
#     try:
#         conn = psycopg2.connect(
#             host="172.16.1.236",
#             port="5432",
#             database="bctst",
#             user="vinayak",
#             password="vinayak"
#         )
#         cur = conn.cursor()
#         print("database connected")
#         return cur, conn
#     except (Exception, psycopg2.Error) as error:
#         print("Failed connected due to: ", error)
#         return cur, conn


@app.route("/insert", methods=["GET", "POST"])      # CREATE an account
def create_account():
    # url = request.url
    cur, conn = set_connection()

    if request.method == "POST":
        # Inserting values into it
        holder_name = request.json["holderName"]
        account_type = request.json["accountType"]
        balance = request.json["balance"]
        postgres_insert_query = """ INSERT INTO bank (holder_name,
                                       account_type,balance) VALUES (%s,%s,%s)"""
        record_to_insert = (holder_name, account_type, balance,)
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
    return jsonify({"message": "Done"}), 200


@app.route("/", methods=["GET"])        # READ the details
def show_list():
    cur, conn = set_connection()
    cur.execute("SELECT * FROM bank")
    data = cur.fetchall()

    return jsonify({"message": data}), 200


# UPDATE (Amount Withdrawal)
@app.route("/withdraw/<int:srno>", methods=["GET", "POST"])
def withdrawal(srno):
    cur, conn = set_connection()

    amount = float(request.json["withdrawAmount"])
    cur.execute("SELECT balance from bank")
    get_balance = cur.fetchall()
    balance = get_balance[srno][0]
    print("get balance", get_balance)

    updated_amt = 0
    if balance > amount:
        updated_amt = balance - amount
        print(updated_amt)
        postgres_query = "UPDATE bank SET balance = %s WHERE srno = %s"
        cur.execute(postgres_query, (updated_amt, srno))
        conn.commit()
    else:
        flash("Insufficient balance")

    print("get balance", get_balance)
    flash("Withdrawal completed")
    return jsonify({"message": "Withdrawal completed", "amount": updated_amt}), 200


@app.route("/deposit/<int:srno>", methods=["GET", "POST"])
def deposit(srno):
    cur, conn = set_connection()
    amount = float(request.json["depositAmount"])

    # balance = float(request.json["balance"])
    cur.execute("SELECT balance from bank")
    get_balance = cur.fetchall()
    balance = get_balance[srno][0]
    print("get balance", get_balance)

    updated_balance = amount + balance
    postgres_query = "UPDATE bank SET balance = %s WHERE srno = %s"
    cur.execute(postgres_query, (updated_balance, srno))
    flash("Amount Deposited")
    conn.commit()
    return jsonify({"message": "Amount Deposited", "amount": updated_balance}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5006)
