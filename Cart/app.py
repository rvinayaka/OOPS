from flask import Flask, request, jsonify
import psycopg2
import logging

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


# create_query = (
#     """CREATE table cart( sno serial PRIMARY KEY,
#                         items VARCHAR(200) NOT NULL,
#                         quantity INTEGER NOT NULL,
#                         price INTEGER NOT NULL );"""
# )

#  sno | items  | quantity | price
# -----+--------+----------+-------
#    1 | Apples |        5 |   300
#    2 | Mango  |        6 |   800
#    3 | KIWI   |       10 |  1000


@app.route("/add", methods=["POST"])             # CREATE an item
def add_to_cart():
    cur, conn = connection()

    try:
        items = request.json["items"]
        quantity = request.json["quantity"]
        price = request.json["price"]

        # input_format = {
        #     "items": "KIWI",
        #     "quantity": 10,
        #     "price": 1000
        # }


        # insert query
        add_query = """INSERT INTO cart(items, 
                            quantity, price) VALUES (%s, %s, %s)"""

        values = (items, quantity, price)

        # execute query
        cur.execute(add_query, values)

        # committing the change done to table
        conn.commit()
        return jsonify({"message": "Added Successfully"}), 201
    except Exception as e:
        logging.warning(f"{e}occurred")
        return jsonify(({"message": e}))
    finally:
        # close the database connection
        conn.close()
        cur.close()



@app.route("/", methods=["GET"])            # READ the cart list
def show_cart():
    cur, conn = connection()

    try:
        show_query = "SELECT * FROM cart;"
        cur.execute(show_query)
        data = cur.fetchall()

        return jsonify({"message": data}), 202
    except Exception as e:
        logging.warning(f"{e} occurred")
        return jsonify(({"message": e}))
    finally:
        conn.close()
        cur.close()


@app.route("/items/<int:sno>", methods=["PUT"])
def update_item_details(sno):
    cur, conn = connection()

    cur.execute("SELECT items from cart where sno = %s", (sno,))
    get_item = cur.fetchone()

    if not get_item:
        return jsonify({"message": "Item not found"}), 200
    data = request.get_json()
    items = data.get('items')
    quantity = data.get('quantity')
    price = data.get('price')

    if items:
        cur.execute("UPDATE cart SET items = %s WHERE sno = %s", (items, sno))
    elif quantity:
        cur.execute("UPDATE cart SET quantity = %s WHERE sno = %s", (quantity, sno))
    elif price:
        cur.execute("UPDATE cart SET price = %s WHERE sno = %s", (price, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data})


@app.route("/checkout", methods=["GET", "POST"])    # Calculate the total price
def checkout():
    cur, conn = connection()

    cur.execute("SELECT SUM(price*quantity) FROM cart;")
    total_price = cur.fetchone()
    print(total_price)
    return jsonify({"message": "Total calculated", "total": "total_price"}), 200


@app.route("/delete/<int:sno>", methods=["GET", "DELETE"])      # DELETE an item from cart
def delete_items(sno):
    cur, conn = connection()
    # get_item_query = "SELECT * FROM cart WHERE sno = %s"
    # cur.execute(get_item_query, (sno, ))

    # get_item = cur.fetch_all()
    # print(get_item)

    if request.method == "DELETE":
        delete_query = "DELETE from cart WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()

    return jsonify({"message": "Deleted Successfully", "items_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
