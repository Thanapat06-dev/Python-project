import sqlite3
from flask import Flask, render_template_string
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Set API & City
load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = "Bangkok"

app = Flask(__name__)

# --- ฟังก์ชันการจัดการ Database --- #
def init_db():
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()

    # สร้างตาราง
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, 
                  temp REAL, 
                  description TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(temp, desc):
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO logs (timestamp, temp, description) VALUES (?, ?, ?)",(now, temp, desc))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("weather_history.db")
    c = conn.cursor()

    # ดึงข้อมูล (10 รายการ)
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 10")
    data = c.fetchall()
    conn.close()
    return data

# --- Route หลัก --- #
@app.route("/")
def home():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    current_weather = ""
    if res.status_code == 200:
        data = res.json()
        temp = data["main"]["temp"]
        desc = data["main"][0]["description"]

        save_to_db(temp, desc)
        current_weather = f"<h3>Current: {temp}°C ({desc})</h3>"

    history = get_history()
    history_html = "".join([f"<tr><td>{row[1]}</td><td>{row[2]}°C</td><td>{row[3]}</td></tr>" for row in history])

    html_page = f"""
    <html>
        <body style="font-family: sans-serif; text-align: center;">
            <h1>📜 Weather History Logger</h1>
            {current_weather}
            <hr>
            <h2>Recent Logs</h2>
            <table border="1" style="margin: auto; width: 80%;">
                <tr><th>Time</th><th>Temp</th><th>Condition</th></tr>
                {history_html}
            </table>
            <br>
            <a href="/">Refresh & Log Again</a>
        </body>
    </html>
    """

    return html_page

if __name__ == "__main__":
    init_db() # สร้าง db ก่อนรัน server
    app.run(debug=True)