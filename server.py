from flask import Flask, request
import requests
import threading
import time

# تنظیمات ربات تلگرام
BOT_TOKEN = "8843330465:AAFhIxoZof8wribids42_XkbIoRhT4fgWrs"
CHAT_ID = "5394676283"

app = Flask(__name__)

# وبهوک تریدینگ‌ویو (اگر بعداً خواستی از TV هم استفاده کنی)
@app.route('/tvwebhook', methods=['POST'])
def tvwebhook():
    data = request.json
    price = data.get("price")
    symbol = data.get("symbol")
    time_tv = data.get("time")

    text = (
        f"📈 سیگنال از تریدینگ‌ویو\n"
        f"نماد: {symbol}\n"
        f"قیمت: {price}\n"
        f"زمان: {time_tv}\n\n"
        f"در حال ساخت تحلیل VIP..."
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text}
    )

    return "OK"

# پینگ برای بیدار نگه داشتن سرور
@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

# تابع گرفتن قیمت لحظه‌ای طلا از API رایگان
def fetch_price_loop():
    while True:
        try:
            # API رایگان نرخ XAU به USD
            r = requests.get("https://api.exchangerate.host/latest?base=XAU&symbols=USD", timeout=10)
            data = r.json()
            price = data["rates"]["USD"]

            text = (
                f"📈 قیمت لحظه‌ای طلا (XAUUSD)\n"
                f"💰 قیمت: {price:.2f} دلار\n\n"
                f"🧠 تحلیل VIP:\n"
                f"- روند کلی: بررسی مقاومت و حمایت\n"
                f"- مراقب شکست سطح‌های مهم باش.\n"
            )

            # ارسال به تلگرام
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": CHAT_ID, "text": text}
            )

        except Exception as e:
            # اگر خطا شد، فقط رد می‌کنیم تا حلقه ادامه پیدا کند
            print("Error in fetch_price_loop:", e)

        # هر 60 ثانیه یک‌بار آپدیت
        time.sleep(60)

# اجرای حلقهٔ گرفتن قیمت در یک ترد جدا
def start_background_tasks():
    t = threading.Thread(target=fetch_price_loop, daemon=True)
    t.start()

# اجرای سرور
if __name__ == "__main__":
    start_background_tasks()
    app.run(host="0.0.0.0", port=10000)
