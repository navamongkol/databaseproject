
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)
con = psycopg2.connect(database="ddbj32ceskaj87", user="rptqqpzboaabxm", password="28e409d190c7576459aa6a9d814798a99ca27b6d839eb5796e8ebf4381bb6af7", host="ec2-54-166-242-77.compute-1.amazonaws.com", port="5432")

@app.route("/test")
def home():
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT* from Members")
    rows = cur.fetchall()
    print(rows)
    return jsonify(rows);

if __name__ == "__main__":
    app.run(debug=True)

