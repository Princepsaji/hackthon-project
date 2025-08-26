from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Local database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=hackathon_db user=postgres password=12345 host=localhost port=5432"
)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode="disable")
    return conn

# ✅ Create table when the app starts
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    description = request.form["description"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()   # ✅ ensures tasks table exists before anything else
    app.run(debug=True)
