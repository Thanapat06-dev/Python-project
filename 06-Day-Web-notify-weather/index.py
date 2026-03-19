from flask import Flask, render_template_string
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# Set API & City
API_KEY = os.getenv("API_KEY")
CITY = "Bangkok"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

# --- Route หลัก (หน้าบ้าน) --- #
@app.route("/")
def home():
    data = get_weather()
    if data:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']

        html_content = f"""
        <html>
            <head>
                <title>Weather Dashboard</title>
            </head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1>☁️ Weather in {CITY}</h1>
                <p style="font-size: 20px;">Temperature: <b>{temp}°C</b></p>
                <p>Condition: {desc.capitalize()}</p>

                <hr style="margin: 20px auto; width: 50%;">

                <a href="/notify" style="padding: 10px 20px; background-color: #7289da; color: white; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Send to Discord
                </a>
            </body>
        </html>
        """
        return html_content
    return "Error: Could not fetch weather data."

# --- Route สำหรับกดส่งไปยัง Discord --- #
@app.route("/notify")
def notify():
    data = get_weather()
    if data:
        msg = f"Report from web: {CITY} is {data['main']['temp']}°C"
        requests.post(DISCORD_WEBHOOK_URL, json={"content" : msg})
        return "<h3>🚀 Sent to Discord!</h3> <a href='/'>Back to Home</a>"
    return "Error: failed to send."

if __name__ == "__main__":
    app.run(debug=True)