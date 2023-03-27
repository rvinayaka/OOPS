from flask import Flask, jsonify, request
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
        # print(cur, conn)
        return cur, conn
    except(Exception, psycopg2.Error) as error:
        print("Failed connection", error)
        return cur, conn

# Online game - Design a class to manage an online game,
# including character creation, game mechanics, and player interactions.

# Query
# CREATE TABLE game(sno SERIAL PRIMARY KEY, character VARCHAR(200) NOT NULL ,
# mechanics VARCHAR(300), interactions VARCHAR(500));

# Game
#  sno | character |     mechanics     |    interactions
# -----+-----------+-------------------+---------------------
#    1 | Naruto    | walk, jump, crawl | synergy, chat
#    2 | Hinata    | battle, run       | Call,
#    3 | Akamaru   | smell, bark       | sign language,
#    4 | Anya      | think, attack     | hypnosis, magnetize

@app.route("/characters", methods=["GET", "POST"])
def create_character():
    cur, conn = db_connection()
    if request.method == "POST":
        char = request.json["char"]
        mech = request.json["mech"]
        interact = request.json["interact"]

        query = """INSERT INTO game(character, mechanics,
                            interactions) VALUES (%s, %s, %s)"""
        values = (char, mech, interact)
        cur.execute(query, values)

        conn.commit()
        conn.close()
        cur.close()
    return jsonify({"message": "Character added"}), 200


@app.route("/", methods=["GET"])  # READ the cart list
def show_all_characters():
    cur, conn = db_connection()

    show_query = "SELECT * FROM game;"
    cur.execute(show_query)
    data = cur.fetchall()

    return jsonify({"message": data}), 200


@app.route("/characters/<int:sno>", methods=["PUT"])
def update_character(sno):
    cur, conn = db_connection()

    cur.execute("SELECT character from game where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    char = data.get('char')
    mech = data.get('mech')
    interact = data.get('interact')

    if char:
        cur.execute("UPDATE game SET character = %s WHERE sno = %s", (char, sno))
    elif mech:
        cur.execute("UPDATE game SET mechanics = %s WHERE sno = %s", (mech, sno))
    elif interact:
        cur.execute("UPDATE game SET interactions = %s WHERE sno = %s", (interact, sno))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"data": data})

@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE an item from cart
def delete_student(sno):
    cur, conn = db_connection()

    if request.method == "DELETE":
        delete_query = "DELETE from game WHERE sno = %s"
        cur.execute(delete_query, (sno,))
        conn.commit()
    return jsonify({"message": "Deleted Successfully", "char no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
