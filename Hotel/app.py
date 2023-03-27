from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

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

# Question:
# Design a class to manage hotel bookings,
# including room availability, reservations, and cancellations.


# Query:
# CREATE room_id details AS (name VARCHAR (100), mobile_no INTEGER, city VARCHAR (100));

# CREATE TABLE hotel(id SERIAL PRIMARY KEY, guest_details details, checkin DATE NOT NULL,
# checkout DATE NOT NULL, status VARCHAR(300));


# Table:
#  id |          guest_details           | room_id |  checkin   |  checkout  | status
# ----+----------------------------------+---------+------------+------------+--------
#   1 | (Naruto,5552304,"LEAF village")  |     101 | 2023-04-05 | 2023-04-10 | booked
#   3 | (Chiraku,2224123,"Sand Village") |     102 | 2022-08-15 | 2022-09-19 | booked
#   2 | (Hinata,9004114,"Water Village") |     102 | 2022-09-12 | 2022-12-09 | booked


@app.route('/guests', methods=["GET", "POST"])
def add_member():           # adding new people who have taken the things from hotel
    cur, conn = connection()

    if request.method == "POST":
        guest_details = request.json["details"]
        room_id = request.json["roomId"]
        checkin = request.json["checkin"]
        checkout = request.json["checkout"]
        status = request.json["status"]

        # input_format:{
        #     "details": {
        #         "name": "Chiraku",
        #         "mobile_no": 2224123,
        #         "city": "Sand Village"
        #     },
        #     "roomId": 102,
        #     "checkin": "2022-08-15",
        #     "checkout": "2022-09-19",
        #     "status": "booked"
        # }

        print(guest_details, room_id, checkin, checkout, status)

        add_query = """INSERT INTO hotel(guest_details, room_id, checkin, checkout, 
                            status)VALUES(ROW(%s, %s, %s)::details, %s, %s::date, %s::date, %s);"""

        values = (guest_details["name"], guest_details["mobile_no"], guest_details["city"], room_id,
                  checkin, checkout, status)
        cur.execute(add_query, values)
        conn.commit()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])            # READ the cart list
def show_entries():
    cur, conn = connection()

    show_query = "SELECT * FROM hotel;"
    cur.execute(show_query)
    data = cur.fetchall()
    print("LIST", data)

    return jsonify({"message": data}), 200


@app.route("/rooms/<int:id>", methods=["PUT"])
def update_details(id):                  # Update the details
    cur, conn = connection()

    cur.execute("SELECT room_id from hotel where id = %s", (id,))
    get_room_id = cur.fetchone()

    if not get_room_id:
        return jsonify({"message": "Details not found"}), 200

    data = request.get_json()
    guest_details = data.get('details')
    checkin = data.get('checkin')
    checkout = data.get('checkout')
    status = data.get('status')

    if guest_details:
        cur.execute("UPDATE hotel SET guest_details = ROW(%s, %s, %s)::details WHERE id = %s",
                    (guest_details['name'], guest_details['mobile_no'], guest_details['city'], id))
    elif checkin:
        cur.execute("UPDATE hotel SET checkin = %s WHERE id = %s", (checkin, id))
    elif checkout:
        cur.execute("UPDATE hotel SET checkout = %s WHERE id = %s", (checkout, id))
    elif status:
        cur.execute("UPDATE hotel SET status = %s WHERE id = %s", (status, id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data, "message": "Details update successfully"}), 200


@app.route("/delete/<int:id>", methods=["DELETE"])      # DELETE an item from cart
def delete_items(id):
    cur, conn = connection()

    if request.method == "DELETE":
        delete_query = "DELETE from hotel WHERE id = %s"
        cur.execute(delete_query, (id,))
        conn.commit()

    return jsonify({"message": "Deleted Successfully", "items_no": id}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000)



