from flask import Flask, flash, request, jsonify
from conn import set_connection         # fetching the connection from other file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'


#  srno | holder_name | account_type | balance
# ------+-------------+--------------+---------
#     3 | Naruto      | Savings      |    3000
#     1 | akshith     | savings      |    3000
#     2 | Naruto      | Savings      |    3200
#     6 | Akamaru     | Current      |    6000

@app.route("/insert", methods=["GET", "POST"])      # CREATE an account
def create_account():
    # start the database connection
    cur, conn = set_connection()

    try:
        # accept only POST method
        if request.method == "POST":
            # Take value from the user
            holder_name = request.json["holderName"]
            account_type = request.json["accountType"]
            balance = request.json["balance"]

            # insert query
            postgres_insert_query = """ INSERT INTO bank (holder_name,
                                           account_type,balance) VALUES (%s,%s,%s)"""
            record_to_insert = (holder_name, account_type, balance,)

            # execute the query with required values
            cur.execute(postgres_insert_query, record_to_insert)

            # commit to database
            conn.commit()

            # close the database connection
            conn.close()
            cur.close()
        return jsonify({"message": "Done"}), 200
    except Exception as error:
        return jsonify({"message": error})


    # input_format = {
    #     "holderName": "Akamaru",
    #     "accountType": "Current",
    #     "balance": 6000
    # }


@app.route("/", methods=["GET"])        # READ the details
def show_list():
    # start the database connection
    cur, conn = set_connection()

    # execute the query to fetch all values
    cur.execute("SELECT * FROM bank")
    data = cur.fetchall()

    # close the database connection
    conn.close()
    cur.close()
    cur.close()
    return jsonify({"message": data}), 200


# UPDATE (Amount Withdrawal)
@app.route("/withdraw/<int:srno>", methods=["GET", "PUT"])
def withdrawal(srno):
    # start the database connection
    cur, conn = set_connection()

    # fetch the balance from table
    cur.execute("SELECT balance from bank WHERE srno = %s", (srno, ))
    get_balance = cur.fetchall()
    balance = get_balance[0][0]
    print("get balance", get_balance)
    print("before", balance)

    # get the amount from the user to deduct the balance
    amount = float(request.json["withdrawAmount"])

    # input_format = {
    #     "withdrawAmount": 2000
    # }

    updated_amt = 0
    if balance > amount:            # only if balance is greater than the amount
        updated_amt = balance - amount
        print("after", updated_amt)

        # execute the query
        postgres_query = "UPDATE bank SET balance = %s WHERE srno = %s"
        cur.execute(postgres_query, (updated_amt, srno))
        conn.commit()
    else:                           # else alert th message
        flash("Insufficient balance")


    flash("Withdrawal completed")

    # close the database connection
    conn.close()
    cur.close()
    return jsonify({"message": "Withdrawal completed", "amount": updated_amt}), 200


@app.route("/deposit/<int:srno>", methods=["GET", "PUT"])
def deposit(srno):
    # start the database connection
    cur, conn = set_connection()

    # fetch the balance from table
    cur.execute("SELECT balance from bank WHERE srno = %s", (srno, ))
    get_balance = cur.fetchall()
    balance = get_balance[0][0]
    print("get balance", get_balance)
    print("after", balance)

    # input_format = {
    #     "depositAmount": 2000
    # }


    # get the amount to be added to the balance
    amount = float(request.json["depositAmount"])

    # update the balance
    updated_balance = amount + balance

    # execute the query
    postgres_query = "UPDATE bank SET balance = %s WHERE srno = %s"
    cur.execute(postgres_query, (updated_balance, srno))
    print("after", updated_balance)
    flash("Amount Deposited")
    conn.commit()

    # close the database connection
    conn.close()
    cur.close()
    return jsonify({"message": "Amount Deposited", "amount": updated_balance}), 200


@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE account from the list
def delete_account(sno):
    # start the database connection
    cur, conn = set_connection()

    if request.method == "DELETE":
        # execute the delete query
        delete_query = "DELETE from bank WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()

        # close the database connection
        conn.close()
        cur.close()
    return jsonify({"message": "Deleted Successfully", "items_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
