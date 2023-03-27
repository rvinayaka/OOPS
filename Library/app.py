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


@app.route("/<string:type>/<int:sno>", methods=["PUT"])
def update_details(sno):
    cur, conn = connection()

    cur.execute("SELECT type from library where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    type = data.get('type')
    borrowed_on = data.get('borrowedOn')
    returned = data.get('returned')

    if type:
        cur.execute("UPDATE library SET type = %s WHERE sno = %s", (type, sno))
    elif borrowed_on:
        cur.execute("UPDATE library SET borrowed_on = %s WHERE sno = %s", (borrowed_on, sno))
    elif returned:
        cur.execute("UPDATE library SET returned = %s WHERE sno = %s", (returned, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data})

@app.route("/", methods=["GET"])            # READ the cart list
def show_entries():
    cur, conn = connection()

    show_query = "SELECT * FROM library;"
    cur.execute(show_query)
    data = cur.fetchall()
    print("LIST", data)

    return jsonify({"message": data}), 200

# @app.route("/library/<int:sno>", methods=["PUT"])
# def update_details(sno):
#     cur, conn = connection()
#
#     cur.execute("SELECT character from library where sno = %s", (sno,))
#     get_character = cur.fetchone()
#
#     if not get_character:
#         return jsonify({"message": "Character not found"}), 200
#     data = request.get_json()
#     char = data.get('char')
#     mech = data.get('mech')
#     interact = data.get('interact')
#
#     if char:
#         cur.execute("UPDATE game SET character = %s WHERE sno = %s", (char, sno))
#     elif mech:
#         cur.execute("UPDATE game SET mechanics = %s WHERE sno = %s", (mech, sno))
#     elif interact:
#         cur.execute("UPDATE game SET interactions = %s WHERE sno = %s", (interact, sno))
#
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     return jsonify({"data": data})


@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE an item from cart
def delete_items(sno):
    cur, conn = connection()

    if request.method == "DELETE":
        delete_query = "DELETE from library WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()

    return jsonify({"message": "Deleted Successfully", "items_no": sno}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000)
