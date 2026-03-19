import sqlite3
from flask import Flask, render_template_string, request, redirect
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")
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
        logs = conn.execute("SELECT * FROM logs WHERE description LIKE ? OR timestamp LIKE ? ORDER BY id DESC",
                            ('%'+search_query+'%', '%'+search_query+'%')).fetchall()
    else:
        logs = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 20").fetchall()

    conn.close()

    history_html = ""
    for row in logs:
        history_html += f"""
        <tr>
            <td>{row['timestamp']}</td>
            <td>{row['temp']}°C</td>
            <td>{row['description']}</td>
            <td><a href="/delete/{row['id']}" style="color: red;" onclick="return confirm('แน่ใจนะว่าจะลบ?')">Delete</a></td>
        </tr>
        """

    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center;">
            <h1>🔍 Weather Log Manager</h1>
            <form action="/" method="get">
                <input type="text" name="search" placeholder="Search data or weather..." value="{search_query}" />
                <button type="submit">Search</button>
                <a href="/">Clear</a>
            </form>
            <br>
            <table border="1" style="margin: auto; width: 80%;">
                <tr><th>Time</th><th>Temp</th><th>Condition</th><th>Action</th></tr>
                {history_html}
            </table>
            <br>
            <a href="/log-now">➕ Log Current Weather</a>
        </body>
    </html>
    """

@app.route("/delete/<int:id>")
def delete_log(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM logs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/log-now")
def log_now():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        conn = get_db_connection()
        conn.execute("INSERT INTO logs (timestamp, temp, description) VALUES (?, ?, ?)", 
                     (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data['main']['temp'], data['weather'][0]['description']))
        conn.commit()
        conn.close()
    
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)