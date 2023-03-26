from flask import Flask, flash, request, jsonify
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'


def set_connection():
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
        print("database connected")
        return cur, conn
    except (Exception, psycopg2.Error) as error:
        print("Failed connected due to: ", error)
        return cur, conn


# create_query = """CREATE TABLE socials(sno SERIAL PRIMARY KEY ,
#                     username VARCHAR(200) NOT NULL ,
#                     liked BOOL NOT NULL ,
#                     comments VARCHAR(300) NOT NULL);"""

@app.route("/add", methods=["GET", "POST"])  # CREATE an account
def create_user():
    cur, conn = set_connection()  # db connection

    try:
        if request.method == "POST":
            # Inserting values into it
            username = request.json["username"]
            liked = request.json["liked"]
            comments = request.json["comments"]
            postgres_insert_query = """ INSERT INTO socials (username,
                                           liked,comments) VALUES (%s,%s,%s)"""
            record_to_insert = (username, liked, comments,)
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
        return jsonify({"message": "Done"}), 200
    except:
        return jsonify({"message": "request method not found"}), 500


@app.route("/", methods=["GET"])
def get_profile():
    cur, conn = set_connection()
    cur.execute("SELECT * FROM socials")
    data = cur.fetchall()

    return jsonify({"message": data}), 200


@app.route("/<string:username>/like", methods=["GET", "POST"])
def like_post(username):
    cur, conn = set_connection()
    liked = request.json["liked"]

    postgres_query = "UPDATE socials SET liked = %s WHERE username = %s"
    cur.execute(postgres_query, (liked, username))
    conn.commit()
    return jsonify({"message": "post liked"}), 200


@app.route("/<string:username>/comment", methods=["GET", "POST"])
def comment_post(username):
    cur, conn = set_connection()
    comment = request.json["comment"]

    postgres_query = "UPDATE socials SET comments = %s WHERE username = %s"
    cur.execute(postgres_query, (comment, username))
    conn.commit()
    return jsonify({"message": "commented on post"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
