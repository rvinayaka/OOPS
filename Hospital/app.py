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

# Query:
# CREATE TABLE hospital(sno SERIAL PRIMARY KEY ,patient_name VARCHAR(200) NOT NULL,
# admission DATE NOT NULL, treatments VARCHAR(400), discharge DATE NOT NULL);

# Table:
#  sno | patient_name | admission | treatments | discharge
# -----+--------------+-----------+------------+-----------

@app.route("/patients", methods=["GET", "POST"])             # Add patient
def add_details():
    cur, conn = connection()

    if request.method == "POST":
        patient_name = request.json["patient"]
        admission = request.json["admission"]
        treatments = request.json["treatments"]
        discharge = request.json["discharge"]

        add_query = """INSERT INTO hospital(patient_name, admission, treatments,  
                            discharge) VALUES (%s, %s, %s, %s)"""

        values = (patient_name, admission, treatments, discharge)
        cur.execute(add_query, values)
        conn.commit()
    return jsonify({"message": "Added Successfully"}), 200



@app.route("/", methods=["GET"])        # READ the details
def show_list():
    cur, conn = connection()
    cur.execute("SELECT * FROM hospital")
    data = cur.fetchall()

    return jsonify({"message": data}), 200


@app.route("/<string:patient_name>/<int:sno>", methods=["PUT"])
def update_patients_details(sno):          # Update the details of patient
    cur, conn = connection()

    cur.execute("SELECT patient_name from hospital where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    patient_name = data.get('stock_name')
    admission = data.get('admission')
    treatments = data.get('treatments')
    discharge = data.get('discharge')
    balance = data.get('balance')

    if patient_name:
        cur.execute("UPDATE hospital SET patient_name = %s WHERE sno = %s", (patient_name, sno))
    elif admission:
        cur.execute("UPDATE hospital SET admission = %s WHERE sno = %s", (admission, sno))
    elif treatments:
        cur.execute("UPDATE hospital SET treatments = %s WHERE sno = %s", (treatments, sno))
    elif discharge:
        cur.execute("UPDATE hospital SET losses = %s WHERE sno = %s", (discharge, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data})


@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE an item from cart
def delete_items(sno):
    cur, conn = connection()

    if request.method == "DELETE":
        delete_query = "DELETE from hospital WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()

    return jsonify({"message": "Deleted Successfully", "items_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
