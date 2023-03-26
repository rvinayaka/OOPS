from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)
# Library management system - Design a class to manage library resources,
# including books, journals, and magazines, borrowing, and returning books.


def connection():           # Database connection
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


@app.route('/add', methods=["GET", "POST"])
def add_member():           # adding new people who have taken the things from library
    cur, conn = connection()

    if request.method == "POST":
        type = request.json["type"]
        borrowed_on = request.json["borrowDate"]
        returned = request.json["returned"]

        print(type, borrowed_on, returned)

        add_query = """INSERT INTO library(type, 
                            borrowed_on, returned) VALUES (%s, %s, %s)"""
        values = (type, borrowed_on, returned)
        cur.execute(add_query, values)
        conn.commit()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])            # READ the cart list
def show_entries():
    cur, conn = connection()

    show_query = "SELECT * FROM library;"
    cur.execute(show_query)
    data = cur.fetchall()
    print("LIST", data)

    return jsonify({"message": data}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
