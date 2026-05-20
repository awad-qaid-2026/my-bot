import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import requests
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote  

# --- [تم الإبقاء على إعداداتك كما هي] ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  
bot = telebot.TeleBot(API_TOKEN)
# ... [بقية إعداداتك الأصلية] ...

# --- الدالة الجديدة لجلب الكود الحقيقي (الذكية) ---
def get_real_sms_code(phone_number):
    try:
        # تنظيف الرقم للبحث (إزالة +)
        clean_num = phone_number.replace("+", "")
        url = f"https://sms-receive.net/free-sms-numbers/{clean_num}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # البحث عن أول رسالة في الجدول
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    message = cols[2].text.strip()
                    # استخراج الكود إذا وجد (يبحث عن أرقام من 4 إلى 6 خانات)
                    code_match = re.search(r'\b\d{4,6}\b', message)
                    if code_match:
                        return f"الرسالة: {message} \n🔑 الكود هو: {code_match.group()}"
            return "لم يصل كود جديد بعد، انتظر 30 ثانية..."
    except Exception as e:
        return "خطأ في الاتصال بالموقع، حاول مجدداً."
    return "لا توجد رسائل حالياً."

# --- [دمج الدالة في handle_queries] ---
# استبدل الجزء الخاص بـ fotp_ في الكود السابق بهذا الجزء:

    elif call.data.startswith("fotp_"):
        _, target_phone, target_svc = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري الفحص في الموقع الآن...")
        
        # استدعاء الدالة الجديدة
        result = get_real_sms_code(target_phone)
        
        # إرسال النتيجة
        try:
            bot.send_message(call.message.chat.id, f"📞 الرقم: `{target_phone}`\n\n📢 النتيجة:\n{result}", parse_mode="Markdown")
            # إرسال للقناة إذا وجد كود
            if "الكود هو" in result:
                bot.send_message(CHANNEL_LOG_ID, f"🔥 **كود مجاني جديد تم سحبه:**\n\n📞 الرقم: `{target_phone}`\n{result}")
        except: pass

# ... [بقية الكود الخاص بك دون تغيير] ...
