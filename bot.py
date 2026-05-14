import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import concurrent.futures

# --- الإعدادات ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
DEVELOPER_TEXT = "اིلཻمຼقᮭن྄༹ع🎭"
bot = telebot.TeleBot(API_TOKEN)

# قائمة شاملة لأكثر من 23 دولة مع أكوادها
COUNTRIES = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷",
    "1249": "Canada 🇨🇦", "31": "Netherlands 🇳🇱", "46": "Sweden 🇸🇪", "34": "Spain 🇪🇸",
    "39": "Italy 🇮🇹", "48": "Poland 🇵🇱", "358": "Finland 🇫🇮", "45": "Denmark 🇩🇰",
    "32": "Belgium 🇧🇪", "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "61": "Australia 🇦🇺",
    "60": "Malaysia 🇲🇾", "62": "Indonesia 🇮🇩", "63": "Philippines 🇵🇭", "66": "Thailand 🇹🇭",
    "852": "Hong Kong 🇭🇰", "27": "South Africa 🇿🇦", "372": "Estonia 🇪🇪", "371": "Latvia 🇱🇻"
}

# روابط المواقع التي يسحب منها البوت (ربط متعدد لضمان توفر الأرقام)
SOURCES = [
    "https://receive-smss.com/free-sms-numbers/",
    "https://sms-online.co/receive-free-sms/",
    "https://receive-sms.cc/India-Phone-Number/"
]

def fetch_from_source(url, code):
    nums = []
    try:
        res = requests.get(f"{url}{code}", timeout=3)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.find_all(['h4', 'a', 'span']):
            txt = item.text.strip().replace(" ", "")
            if txt.startswith(f'+{code}') and 10 < len(txt) < 16:
                nums.append(txt)
    except: pass
    return nums

def get_all_numbers(code):
    all_nums = []
    # استخدام ThreadPoolExecutor للبحث في كل المواقع في نفس الوقت (سرعة خارقة)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_from_source, url, code) for url in SOURCES]
        for future in concurrent.futures.as_completed(futures):
            all_nums.extend(future.result())
    return list(set(all_nums))[:15] # حذف المكرر وأخذ أول 15 رقم

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WhatsApp_🟢"),
        types.InlineKeyboardButton("🔵 Facebook", callback_data="svc_Facebook_🔵"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="svc_Telegram_✈️"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_Instagram_📸"),
        types.InlineKeyboardButton("🎵 TikTok", callback_data="svc_TikTok_🎵"),
        types.InlineKeyboardButton(f"👨‍💻 تواصل مع المطور {DEVELOPER_TEXT}", url="https://t.me/Your_Username") # ضع يوزرك هنا
    )
    bot.send_message(message.chat.id, "⚔️ **بوت دمار المقنع للأرقام**\nاختر الخدمة التي تريدها:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("svc_"))
def select_country(call):
    service = call.data.split("_")[1]
    icon = call.data.split("_")[2]
    markup = types.InlineKeyboardMarkup(row_width=2)
    # توليد أزرار الدول (أكثر من 23 دولة)
    btns = [types.InlineKeyboardButton(name, callback_data=f"get_{service}_{code}_{icon}") for code, name in COUNTRIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_main"))
    bot.edit_message_text(f"{icon} **خدمة {service}**\nاختر الدولة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def show_nums(call):
    _, service, code, icon = call.data.split("_")
    bot.answer_callback_query(call.id, "🚀 جاري سحب الأرقام فوراً...")
    
    nums = get_all_numbers(code)
    
    if nums:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for n in nums:
            markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
        markup.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{service}_{icon}"))
        bot.edit_message_text(f"✅ **أرقام {service} المتاحة:**\nاضغط على الرقم لنسخه واستخدامه:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❌ الأرقام لهذه الدولة مشغولة حالياً، جرب دولة أخرى", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_home(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def handle_copy(call):
    num = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"تم اختيار الرقم: {num}\nاستخدمه الآن لتفعيل الحساب!", show_alert=True)

bot.infinity_polling()
