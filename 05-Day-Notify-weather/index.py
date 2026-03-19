import requests

# --- 1. ส่วนของการตั้งค่า Configuration --- #
# Set API & City
API_KEY = "77266b5b09139c59c88aa5639b8d1b6b"
CITY = "Bangkok"

# เชื่อมต่อกับ Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1483661538744209419/TuEIzrOD2gq_s3sb9o7zOYGEFD9rhSOnuKY0zZw0rsO006qvhWcVIASmiJXwCp--SmZJ"

# --- 2. ฟังก์ชันสำหรับการส่งข้อมูลไปยัง Discord --- #
def send_discord_notify(message):
    # discord รับข้อมูลเป็น json ที่มี 'key' เป็น content
    data = {
        "content" : message,
        "username" : "Weather Bot" # สามารถเปลี่ยนชื่อ บอทได้ตรงนี้
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code

# --- 3. การทำงานหลัก --- #
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    res = requests.get(weather_url)

    if res.status_code == 200:
        d = res.json()
        temp = d['main']['temp']
        desc = d['weather'][0]['description']

        # ส่วนของการตกแต่ง
        msg = (
            f"**------- สภาพอากาศประจำวัน ------** \n"
            f"📍 ** เมือง : {CITY} ** \n"
            f"🌡️ ** อุณหภูมิ : {temp} ** \n"
            f"☁️ ** สภาพอากาศ : {desc.capitalize()} ** \n"
            f"--------------------------------------"
        )

        status = send_discord_notify(msg)
        if status == 204:
            print("🚀 ส่งรายการเข้า Discord เรียบร้อยแล้ว")
        else:
            print(f"❌ ส่งข้อมูลไม่สำเร็จ Status: {status}")

except Exception as e:
    print(f"⚠️ Error: {e}")