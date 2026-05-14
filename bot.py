import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os

# إعدادات البوت الأساسية
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188 # ايديك يا عواد
bot = telebot.TeleBot(API_TOKEN)

# قائمة القنوات للاشتراك الإجباري
CHANNELS = ["@v_o_lti", "@jzbznznx", "@bsbsb8_djbd"]

# قاعدة بيانات الدول والمفاتيح الخاصة بها
COUNTRIES = {
    "usa": {"name": "أمريكا 🇺🇸", "code": "1"},
    "uk": {"name": "بريطانيا 🇬🇧", "code": "44"},
    "france": {"name": "فرنسا 🇫🇷", "code": "33"},
    "sweden": {"name": "السويد 🇸🇪", "code": "46"},
    "malaysia": {"name": "ماليزيا 🇲🇾", "code": "60"},
    "indonesia": {"name": "إندونيسيا 🇮🇩", "code": "62"}
}

def is_subscribed(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: return True

def fetch_all_numbers():
    # دالة لجلب الأرقام من المصادر وتصنيفها
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = ["https://receive-smss.com/", "https://sms-online.co/receive-free-sms"]
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.find_all(['a', 'span', 'td']):
                txt = item.text.strip().replace(" ", "")
                if txt.startswith('+') and 10 < len(txt) < 16:
                    if txt not in nums: nums.append(txt)
        except: continue
    return nums

@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        # إضافة أزرار الدول بناءً على القائمة أعلاه
        buttons = [types.InlineKeyboardButton(c['name'], callback_data=f"country_{k}") for k, c in COUNTRIES.items()]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "🌍 **مرحباً بك في قسم الدول!**\nاختر الدولة التي تريد أرقاماً منها:", reply_markup=markup, parse_mode="Markdown")
    else:
        # أزرار الاشتراك الإجباري في حال عدم الاشتراك
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 قناة 1", url=f"https://t.me/{CHANNELS[0][1:]}"),
            types.InlineKeyboardButton("📢 قناة 2", url="https://t.me/+2eq5lZ_hVhA0NGQ8"),
            types.InlineKeyboardButton("✅ تحقق", callback_data="verify")
        )
        bot.send_message(message.chat.id, "⚠️ **يجب الانضمام للقنوات للمتابعة:**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def show_numbers(call):
    country_key = call.data.split("_")[1]
    country_info = COUNTRIES[country_key]
    bot.answer_callback_query(call.id, f"جاري جلب أرقام {country_info['name']}...")
    
    all_nums = fetch_all_numbers()
    # تصفية الأرقام بناءً على مفتاح الدولة المختار
    filtered = [n for n in all_nums if n.startswith(f"+{country_info['code']}")]
    
    if filtered:
        msg = f"📲 **أرقام متاحة لـ {country_info['name']}:**\n\n"
        msg += "\n".join([f"`{n}`" for n in filtered[:10]])
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_to_list"))
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, f"❌ عذراً، لا توجد أرقام متاحة حالياً لـ {country_info['name']}")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_list")
def back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()
