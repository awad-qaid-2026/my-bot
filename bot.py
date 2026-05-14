import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import time

# --- الإعدادات ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)

# قائمة القنوات (فارغة الآن كما طلبت)
CHANNELS = [] 
DEV_NAME = "(اིلཻمຼقᮭن྄༹ع🎭)"

# قاعدة بيانات الدول المضمونة (أكثر من 23 دولة)
COUNTRIES = {
    "49": "ألمانيا 🇩🇪", "1": "أمريكا 🇺🇸", "44": "بريطانيا 🇬🇧", "33": "فرنسا 🇫🇷",
    "46": "السويد 🇸🇪", "31": "هولندا 🇳🇱", "60": "ماليزيا 🇲🇾", "62": "إندونيسيا 🇮🇩",
    "48": "بولندا 🇵🇱", "34": "إسبانيا 🇪🇸", "7": "روسيا 🇷🇺", "380": "أوكرانيا 🇺🇦",
    "91": "الهند 🇮🇳", "20": "مصر 🇪🇬", "212": "المغرب 🇲🇦", "966": "السعودية 🇸🇦",
    "90": "تركيا 🇹🇷", "81": "اليابان 🇯🇵", "82": "كوريا 🇰🇷", "1787": "بورتوريكو 🇵🇷",
    "1201": "نيوجيرسي 🇺🇸", "41": "سويسرا 🇨🇭", "1416": "كندا 🇨🇦"
}

# تخزين مؤقت للأرقام لزيادة السرعة
cache = {}

def fetch_fast_numbers(code):
    # إذا كانت الأرقام موجودة في الذاكرة من أقل من 5 دقائق، ارسلها فوراً
    if code in cache and time.time() - cache[code]['time'] < 300:
        return cache[code]['nums']

    headers = {'User-Agent': 'Mozilla/5.0'}
    # محركات البحث (سحب من عدة مواقع في نفس الوقت)
    urls = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/Free-SMS-Number/{code}"
    ]
    
    found = []
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=3)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.find_all(['h4', 'a']):
                txt = item.text.strip().replace(" ", "")
                if txt.startswith(f'+{code}') and 10 < len(txt) < 16:
                    if txt not in found: found.append(txt)
            if len(found) > 5: break
        except: continue
    
    cache[code] = {'nums': found, 'time': time.time()}
    return found

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="app_WhatsApp"),
        types.InlineKeyboardButton("🔵 Facebook", callback_data="app_Facebook"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="app_Telegram"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="app_Instagram"),
        types.InlineKeyboardButton("🎭 تواصل مع المطور", url="https://t.me/A_W_A_D_1") # استبدل بليزر حقك
    )
    bot.send_message(message.chat.id, f"⚔️ **أهلاً بك في بوت المقنع**\nمطور البوت: {DEV_NAME}\nالخدمات متاحة 24 ساعة 🚀", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("app_"))
def select_country(call):
    app = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(name, callback_data=f"get_{app}_{code}") for code, name in COUNTRIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back"))
    bot.edit_message_text(f"📍 خدمة: {app}\nاختر الدولة (متوفر 23+ دولة):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def get_final_nums(call):
    _, app, code = call.data.split("_")
    bot.answer_callback_query(call.id, "⚡ جاري السحب السريع...")
    
    nums = fetch_fast_numbers(code)
    
    if nums:
        icons = {"WhatsApp": "🟢", "Facebook": "🔵", "Telegram": "✈️", "Instagram": "📸"}
        icon = icons.get(app, "🔹")
        msg = f"✅ **أرقام {app} المتاحة حالياً:**\n\n"
        markup = types.InlineKeyboardMarkup(row_width=1)
        for n in nums:
            markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
        
        markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"app_{app}"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "❌ هذه الدولة لم تنزل أرقاماً جديدة حالياً، جرب دولة ثانية من القائمة.")

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    welcome(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def copy_num(call):
    num = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"تم نسخ الرقم: {num}\nاستخدمه الآن!", show_alert=True)

bot.infinity_polling()
