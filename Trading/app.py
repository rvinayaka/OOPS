from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


def connection():
    cur, conn = None, None
    try:
        conn = psycopg2.connect(
            host="172.16.1.236",
            port="5432",
            database="bctst",
            user="vinayak",
            password="vinayak"
        )
        cur = conn.cursor()
        print("DB connected")
        print(cur, conn)
        return cur, conn
    except(Exception, psycopg2.Error) as error:
        print("Failed connection", error)
        return cur, conn
# Question
# Stock trading system - Design a class to manage stock trades,
# including buying and selling stocks, calculating profits, and losses.

# Query
# CREATE TABLE stocks(sno SERIAL PRIMARY KEY, stock_name VARCHAR(200) NOT NULL ,
# status VARCHAR(200), profits NUMERIC, losses NUMERIC, balance NUMERIC);

# Table
# sno | stock_name  | status  | returns | balance | calculated
# -----+-------------+---------+---------+---------+------------
#    1 | Adani Power | selling |   -2000 |    2800 | t
#    2 | Tata motors | selling |     150 |    3000 | t
#    3 | Synergy     | buying  |     150 |    1800 | f
#    4 | ITC         | buying  |      80 |    1800 | t


@app.route("/stocks", methods=["GET", "POST"])             # CREATE an stock profile
def add_details():
    cur, conn = connection()

    if request.method == "POST":
        stock_name = request.json["stockName"]
        status = request.json["status"]
        profits = request.json["profits"]
        losses = request.json["losses"]
        balance = request.json["balance"]

        add_query = """INSERT INTO stocks(stock_name, status, profits,  
                            losses, balance) VALUES (%s, %s, %s, %s, %s)"""

        values = (stock_name, status, profits, losses, balance)
        cur.execute(add_query, values)
        conn.commit()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])                            # READ the details of all stocks
def show_list():
    cur, conn = connection()
    cur.execute("SELECT * FROM stocks")
    data = cur.fetchall()

    return jsonify({"message": data}), 200


# @app.route("/<string:stock_name>", methods=["GET"])
# def get_stocks(stock_name):
#     cur, conn = connection()
#     get_query = "SELECT status, balance from stocks WHERE stock_name = %s"
#     values = (stock_name,)
#
#     cur.execute(get_query, values)
#     get_balance = cur.fetchall()
#
#     status = get_balance[0][0]
#     balance = get_balance[0][1]
#
#     print(get_balance, status, balance)
#     return jsonify({"message": "Buying successful"}), 200


@app.route("/<string:stocks_name>/<int:sno>", methods=["PUT"])  # update details of stocks
def update_stock_details(sno):
    cur, conn = connection()

    cur.execute("SELECT stock_name from stocks where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    stock_name = data.get('stock_name')
    status = data.get('status')
    profits = data.get('profits')
    losses = data.get('losses')
    balance = data.get('balance')

    if stock_name:
        cur.execute("UPDATE game SET stock_name = %s WHERE sno = %s", (stock_name, sno))
    elif status:
        cur.execute("UPDATE game SET status = %s WHERE sno = %s", (status, sno))
    elif profits:
        cur.execute("UPDATE game SET profits = %s WHERE sno = %s", (profits, sno))
    elif losses:
        cur.execute("UPDATE game SET losses = %s WHERE sno = %s", (losses, sno))
    elif balance:
        cur.execute("UPDATE game SET balance = %s WHERE sno = %s", (balance, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data}), 200


@app.route("/returns/<string:stock_name>", methods=["GET", 'PUT'])       # calculate returns of each stock
def calc_returns(stock_name):
    try:
        cur, conn = connection()
        get_query = "SELECT status, balance from stocks WHERE stock_name = %s"
        values = (stock_name,)

        cur.execute(get_query, values)
        get_balance = cur.fetchall()

        status = get_balance[0][0]
        balance = get_balance[0][1]

        print(get_balance, status, balance)

        if request.method == "PUT":
            if status == "buying":
                returns = request.json["returns"]
                updated_bal = balance + returns

                query = """UPDATE stocks SET balance = %s WHERE stock_name = %s"""
                values = (updated_bal, stock_name)

                cur.execute(query, values)
                conn.commit()

        return jsonify({"message": "Balance updated"}), 200
    except ValueError:
        return jsonify({"message": "Endpoints not found"})
    # except TypeError:
    #     return jsonify({"not all arguments converted during string formatting"})


@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE an item from cart
def delete_stocks(sno):
    cur, conn = connection()

    if request.method == "DELETE":
        delete_query = "DELETE from stocks WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()
    return jsonify({"message": "Deleted Successfully", "char no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
