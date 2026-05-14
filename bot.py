import telebot
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from telebot import types

# --- الإعدادات ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
DEVELOPER_ID = "8388141188" # ايديك الشخصي
bot = telebot.TeleBot(API_TOKEN)

# قائمة المواقع العالمية لضمان وجود أرقام دائماً
SMS_SOURCES = [
    "https://receive-smss.com/free-sms-numbers/",
    "https://sms-online.co/receive-free-sms/",
    "https://receive-sms.cc/",
    "https://anonymisms.com/",
    "https://temp-number.com/countries/"
]

# قائمة الدول الـ 23 (الأكثر طلباً)
COUNTRIES = {
    "1": "USA 🇺🇸", "44": "UK 🇬🇧", "49": "Germany 🇩🇪", "33": "France 🇫🇷",
    "7": "Russia 🇷🇺", "48": "Poland 🇵🇱", "31": "Netherlands 🇳🇱", "46": "Sweden 🇸🇪",
    "1249": "Canada 🇨🇦", "34": "Spain 🇪🇸", "39": "Italy 🇮🇹", "60": "Malaysia 🇲🇾",
    "62": "Indonesia 🇮🇩", "66": "Thailand 🇹🇭", "84": "Vietnam 🇻🇳", "351": "Portugal 🇵🇹",
    "43": "Austria 🇦🇹", "41": "Switzerland 🇨🇭", "32": "Belgium 🇧🇪", "45": "Denmark 🇩🇰",
    "358": "Finland 🇫🇮", "353": "Ireland 🇮🇪", "995": "Georgia 🇬🇪"
}

def scrape_site(url, code):
    nums = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(f"{url}{code}", headers=headers, timeout=3)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.find_all(['h4', 'a', 'span', 'td']):
            txt = item.text.strip().replace(" ", "")
            if txt.startswith(f'+{code}') and 10 < len(txt) < 16:
                nums.append(txt)
    except: pass
    return nums

def get_fast_numbers(code):
    all_found = []
    # البحث في كل المواقع في وقت واحد (سرعة خارقة)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_site, site, code) for site in SMS_SOURCES]
        for future in concurrent.futures.as_completed(futures):
            all_found.extend(future.result())
    return list(set(all_found)) # حذف المكرر

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="app_WA"),
        types.InlineKeyboardButton("🔵 Facebook", callback_data="app_FB"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="app_TG"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="app_IG"),
        types.InlineKeyboardButton("🎵 TikTok", callback_data="app_TK"),
        types.InlineKeyboardButton("🎭 تواصل مع المطور", url=f"tg://user?id={DEVELOPER_ID}")
    )
    bot.send_message(message.chat.id, "⚔️ **مرحباً بك في بوت المقنع للأرقام**\nاختر الخدمة التي تريد تفعيلها:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("app_"))
def select_country(call):
    service = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(name, callback_data=f"get_{service}_{code}") for code, name in COUNTRIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 عودة للرئيسية", callback_data="home"))
    bot.edit_message_text(f"📍 **الخدمة المختارة:** {service}\nاختر الدولة (متوفر 23 دولة):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def fetch_now(call):
    _, service, code = call.data.split("_")
    bot.answer_callback_query(call.id, "🚀 جاري سحب الأرقام فوراً...")
    
    nums = get_fast_numbers(code)
    
    if nums:
        markup = types.InlineKeyboardMarkup(row_width=1)
        icon = "🟢" if service == "WA" else "🔵"
        for n in nums[:15]:
            markup.add(types.InlineKeyboardButton(f"{icon} {n}", callback_data=f"copy_{n}"))
        markup.add(types.InlineKeyboardButton("🔙 جرب دولة أخرى", callback_data=f"app_{service}"))
        bot.edit_message_text(f"✅ **أرقام {service} الجاهزة:**\nاضغط على الرقم لنسخه واستخدامه:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        # رد ذكي في حال لم يجد أرقاماً في هذه الدولة
        bot.send_message(call.message.chat.id, "❤️‍🩹 **هذه الدولة لم تنزل أرقاماً جديدة حالياً، جرب دولة ثانية من القائمة.**")

@bot.callback_query_handler(func=lambda call: call.data == "home")
def home(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def copied(call):
    bot.answer_callback_query(call.id, "تم اختيار الرقم! انسخه الآن وثبته ✅", show_alert=True)

bot.infinity_polling()
