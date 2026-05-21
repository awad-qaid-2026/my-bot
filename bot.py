import os
import sys
import io
import telebot
from flask import Flask, request
import requests

# 1. حل مشكلة ترميز النصوص العربية ومنع خطأ latin-1 الشائع في السيرفرات
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 2. ضع التوكن الجديد الخاص بك هنا بين علامتي التنصيص
API_TOKEN = '8686242492:AAEg1LcQBk3y3QA0ZOr7B39_58V3jfXSw04'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(name)

# مثال لكيفية إرسال الطلبات لـ API الأرقام بأمان دون أخطاء ترميز
def get_number_from_api(api_url, payload={}):
    try:
        # استخدام التشفير التلقائي للبيانات يمنع خطأ latin-1 تماماً
        response = requests.get(api_url, params=payload, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"حدث خطأ في الاتصال بالسيرفر: {e}")
        return None

# ترحيب بالبث عند الضغط على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # مثال للتأكد من أن النصوص العربية ترسل بسلاسة
    welcome_text = (
        "👑 مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام\n\n"
        "✨ المحرك النفاث نشط الآن ومحدث بالكامل لعام 2026."
    )
    bot.reply_to(message, welcome_text)

# تأكد من تعديل الـ Route والـ Webhook إذا كنت تستخدم Render أو PythonAnywhere
@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # استبدل برابط استضافتك على Render إذا كنت تستخدم الـ Webhook
    # bot.set_webhook(url='https://al-moqana.onrender.com/' + API_TOKEN)
    return "البوت يعمل بنجاح والترميز آمن!", 200

if name == "main":
    # تشغيل السيرفر
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
