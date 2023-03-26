from flask import request, Flask, jsonify
import psycopg2

app = Flask(__name__)

# Employee payroll system - Design a class to manage employee payroll,
# including calculating salaries, taxes, and benefits.


def db_connection():
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


@app.route("/add", methods=["GET", "POST"])             # CREATE an item
def add_employee():
    cur, conn = db_connection()

    if request.method == "POST":
        emp_name = request.json["empName"]
        salary = request.json["salary"]
        taxes = salary * 0.18
        benefits = salary * 0.5
        print(emp_name, salary, taxes, benefits)

        add_query = """INSERT INTO payroll(emp_name, salary, 
                            taxes, benefits) VALUES (%s, %s, %s, %s)"""
        # entry = "{
        #     "empName": "ABCD",
        #     "salary": 4000
        #   }"
        values = (emp_name, salary, taxes, benefits)
        cur.execute(add_query, values)

        conn.commit()
        cur.close()
        conn.close()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])            # READ the cart list
def emp_details():
    cur, conn = db_connection()

    show_query = "SELECT * FROM payroll;"
    cur.execute(show_query)
    data = cur.fetchall()
    print("LIST", data)

    cur.close()
    conn.close()

    return jsonify({"message": data}), 200


@app.route("/delete/<int:sno>", methods=["GET", "DELETE"])
def delete_emp(sno):
    cur, conn = db_connection()

    if request.method == "DELETE":
        query = "DELETE FROM payroll WHERE sno = %s"
        cur.execute(query, (sno,))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
