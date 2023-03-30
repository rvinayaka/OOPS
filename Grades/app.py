from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


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


# Student grading system - Design a class to manage student grades,
# including entering grades, calculating averages, and generating reports.

# CREATE TABLE school(sno SERIAL PRIMARY KEY ,std_name VARCHAR(200) NOT NULL,
# grades INTEGER, average NUMERIC, report_progress VARCHAR(300));

#  sno | std_name | grades | average | report_progress
# -----+----------+--------+---------+------------------
#    1 | Rajguru  |    200 |    78.2 | done calculating
#    2 | SPB      |    250 |      76 | reviewed
#    3 | arijit   |    220 |      71 | evaluating
#    4 | shreya   |    210 |      70 | reviewing
#    6 | Hinata   |    700 |      75 | done

@app.route("/students", methods=["GET", "POST"])  # CREATE an item
def add_student():
    cur, conn = db_connection()

    if request.method == "POST":
        std_name = request.json["stdName"]  # string
        grades = request.json["grades"]  # int
        average = request.json["avg"]  # float
        report_progress = request.json["prog"]  # string

        # format = {
        #     "stdName": "Hinata",
        #     "grades": 700,
        #     "avg": 75,
        #     "prog": "done"
        # }

        add_query = """INSERT INTO school(std_name, grades, 
                            average, report_progress) VALUES (%s, %s, %s, %s)"""

        values = (std_name, grades, average, report_progress)
        cur.execute(add_query, values)
        conn.commit()

        cur.close()
        conn.close()
    return jsonify({"message": "Added Successfully"}), 200


@app.route("/", methods=["GET"])  # READ the cart list
def show_std_grades():
    cur, conn = db_connection()

    show_query = "SELECT * FROM school;"
    cur.execute(show_query)
    data = cur.fetchall()

    return jsonify({"message": data}), 200

# @app.route("/grades/<int:sno>", methods=["GET", "PUT"])
# def change_grades(sno):         # updating the grades with average
#     cur, conn = db_connection()
#     try:
#         if request.method == "POST":
#             grades = request.json["grades"]
#             avg = request.json["avg"]
#
#             query = """UPDATE school SET grades = %s, average = %s WHERE sno = %s"""
#
#             values = (grades, avg, sno)
#             cur.execute(query, values)
#             conn.commit()
#
#             cur.close()
#             conn.close()
#
#         return jsonify({"message": "Grades updated"}), 200
#     except TypeError:
#         return jsonify({"message": "error"})

@app.route("/students/<int:sno>", methods=["PUT"])
def update_std_grades(sno):
    cur, conn = db_connection()

    cur.execute("SELECT std_name from school where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Student not found"}), 200
    data = request.get_json()
    std_name = data.get('std_name')
    grades = data.get('grades')
    average = data.get('average')
    report_progress = data.get('report_progress')

    if std_name:
        cur.execute("UPDATE school SET std_name = %s WHERE sno = %s", (std_name, sno))
    elif grades:
        cur.execute("UPDATE school SET grades = %s WHERE sno = %s", (grades, sno))
    elif average:
        cur.execute("UPDATE school SET average = %s WHERE sno = %s", (average, sno))
    elif report_progress:
        cur.execute("UPDATE school SET report_progress = %s WHERE sno = %s", (report_progress, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data})


@app.route("/delete/<int:sno>", methods=["GET", "DELETE"])      # DELETE an item from cart
def delete_student(sno):
    cur, conn = db_connection()

    if request.method == "DELETE":
        delete_query = "DELETE from school WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()
    return jsonify({"message": "Deleted Successfully", "items_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
