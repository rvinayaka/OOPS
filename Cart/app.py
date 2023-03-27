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


create_query = (
    """CREATE table cart( sno serial PRIMARY KEY,
                        items VARCHAR(200) NOT NULL, 
                        quantity INTEGER NOT NULL, 
                        price INTEGER NOT NULL );"""
)


@app.route("/add", methods=["GET", "POST"])             # CREATE an item
def add_to_cart():
    cur, conn = connection()

    if request.method == "POST":
        items = request.json["items"]
        quantity = request.json["quantity"]
        price = request.json["price"]

        add_query = """INSERT INTO cart(items, 
                            quantity, price) VALUES (%s, %s, %s)"""

        values = (items, quantity, price)
        cur.execute(add_query, values)
        conn.commit()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])            # READ the cart list
def show_cart():
    cur, conn = connection()

    show_query = "SELECT * FROM cart;"
    cur.execute(show_query)
    data = cur.fetchall()

    return jsonify({"message": data}), 200


@app.route("/items/<int:sno>", methods=["PUT"])
def update_item_details(sno):
    cur, conn = connection()

    cur.execute("SELECT items from cart where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
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
