import sqlite3
import requests
from flask import Flask, render_template, redirect, request
from datetime import datetime

app = Flask(__name__)

# --- Config --- #
API_KEY = "77266b5b09139c59c88aa5639b8d1b6b"
CITY = "Bangkok"

def get_db_connection():
    conn = sqlite3.connect("weather_history.db")
    conn.row_factory = sqlite3.Row

    return conn

@app.route("/")
def home():
    search_query = request.args.get("search", "")
    conn = get_db_connection()

    if search_query:
        # ค้นหาด้วย SQL LIKE
        logs = conn.execute("SELECT * FROM logs WHERE description LIKE ? ORDER BY id DESC",
                            ('%'+search_query+'%',)).fetchall()
    else:
        logs = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 15").fetchall()

    conn.close()

    return render_template("index.html", logs=logs, search_query=search_query)

@app.route("/log-now")
def log_now():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        conn = get_db_connection()
        conn.execute("INSERT INTO logs (timestamp, temp, description) VALUES (?, ?, ?)", 
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                        data['main']['temp'], 
                        data['weather'][0]['description']))
        
        conn.commit()
        conn.close()

        return redirect("/")
    
@app.route("/delete/<int:id>")
def delete_log(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM logs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)