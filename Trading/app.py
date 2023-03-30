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

#  id | stock_name  | status  | returns | balance | calculated
# ----+-------------+---------+---------+---------+------------
#   1 | Adani Power | selling |   -2000 |    2800 | t
#   2 | Tata motors | selling |     150 |    3000 | t
#   3 | Synergy     | buying  |     150 |    1800 | f
#   4 | ITC         | buying  |      80 |    1800 | t
#   5 | sysco       | buying  |     200 |    1200 |

@app.route("/stocks", methods=["GET", "POST"])             # CREATE a stock profile
def add_new_stock():
    cur, conn = connection()
    try:

        if request.method == "POST":
            stock_name = request.json["stockName"]
            status = request.json["status"]
            returns = request.json["returns"]
            balance = request.json["balance"]
            # format = {
            #     "stockName": "sysco",
            #     "status": "buying",
            #     "returns": 200,
            #     "balance": 1200
            # }

            add_query = """INSERT INTO stocks(stock_name, status,  
                                returns, balance) VALUES (%s, %s, %s, %s)"""

            values = (stock_name, status, returns, balance)
            cur.execute(add_query, values)
            conn.commit()
        return jsonify({"message": "Added Successfully"}), 200
    except KeyError:
        return jsonify({"message": "Keywords didn't match"})


@app.route("/", methods=["GET"])                            # READ the details of all stocks
def show_all_stocks():
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

@app.route("/stocks/<int:id>", methods=["PUT"])  # update details of stocks
def update_stock_details(id):
    cur, conn = connection()

    cur.execute("SELECT stock_name from stocks where id = %s", (id,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    stock_name = data.get('stock_name')
    status = data.get('status')
    returns = data.get('returns')
    balance = data.get('balance')

    if stock_name:
        cur.execute("UPDATE game SET stock_name = %s WHERE id = %s", (stock_name, id))
    elif status:
        cur.execute("UPDATE game SET status = %s WHERE id = %s", (status, id))
    elif returns:
        cur.execute("UPDATE game SET returns = %s WHERE sno = %s", (returns, id))
    elif balance:
        cur.execute("UPDATE game SET balance = %s WHERE sno = %s", (balance, id))

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
def delete_stock(sno):
    cur, conn = connection()

    if request.method == "DELETE":
        delete_query = "DELETE from stocks WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()
    return jsonify({"message": "Deleted Successfully", "char no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
