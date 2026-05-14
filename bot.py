import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import concurrent.futures # للسرعة الخارقة

# --- إعدادات البوت ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
MY_CHANNEL = '@Your_Channel' # ضع معرف قناتك هنا فقط
DEVELOPER_NAME = "اིلཻمຼقᮭن྄༹ع🎭"
ADMIN_ID = 8388141188 # ايديك للتواصل
bot = telebot.TeleBot(API_TOKEN)

# قائمة الـ 23 دولة وأكثر
COUNTRIES = {
    "1": "أمريكا 🇺🇸", "44": "بريطانيا 🇬🇧", "49": "ألمانيا 🇩🇪", 
    "33": "فرنسا 🇫🇷", "46": "السويد 🇸🇪", "31": "هولندا 🇳🇱",
    "61": "أستراليا 🇦🇺", "1249": "كندا 🇨🇦", "34": "إسبانيا 🇪🇸",
    "39": "إيطاليا 🇮🇹", "48": "بولندا 🇵🇱", "32": "بلجيكا 🇧🇪",
    "41": "سويسرا 🇨🇭", "45": "الدنمارك 🇩🇰", "351": "البرتغال 🇵🇹",
    "358": "فنلندا 🇫🇮", "47": "النرويج 🇳🇴", "43": "النمسا 🇦🇹",
    "60": "ماليزيا 🇲🇾", "62": "إندونيسيا 🇮🇩", "66": "تايلاند 🇹🇭",
    "84": "فيتنام 🇻🇳", "91": "الهند 🇮🇳"
}

# مواقع السحب السريع
URLS = [
    "https://receive-smss.com/free-sms-numbers/",
    "https://sms-online.co/receive-free-sms/",
    "https://receive-sms.cc/India-SMS-Number/"
]

def fetch_from_site(url, code):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(f"{url}{code}", headers=headers, timeout=3)
        soup = BeautifulSoup(res.text, 'html.parser')
        nums = []
        for item in soup.find_all(['h4', 'a', 'span']):
            n = item.text.strip().replace(" ", "")
            if n.startswith(f'+{code}') and 10 < len(n) < 16:
                nums.append(n)
        return nums
    except: return []

def get_fast_numbers(code):
    all_found = []
    # البحث في كل المواقع في نفس اللحظة للسرعة
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_from_site, url, code) for url in URLS]
        for future in concurrent.futures.as_completed(futures):
            all_found.extend(future.result())
    return list(set(all_found)) # حذف التكرار

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="app_WA"),
        types.InlineKeyboardButton("🔵 Facebook", callback_data="app_FB"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="app_TG"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="app_IG"),
        types.InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=f"tg://user?id={ADMIN_ID}")
    )
    bot.send_message(message.chat.id, f"⚔️ **أهلاً بك في بوت {DEVELOPER_NAME}**\nاختر التطبيق المطلوب:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("app_"))
def show_countries(call):
    app = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [types.InlineKeyboardButton(name, callback_data=f"num_{app}_{code}") for code, name in COUNTRIES.items()]
    markup.add(*btns)
    markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
    bot.edit_message_text(f"📍 التطبيق: {app}\nاختر الدولة (متوفر 23+ دولة):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("num_"))
def send_numbers(call):
    _, app, code = call.data.split("_")
    bot.answer_callback_query(call.id, "🚀 جاري السحب الصاروخي...")
    
    nums = get_fast_numbers(code)
    
    if nums:
        icon = "🟢" if app == "WA" else "🔵"
        res_text = f"✅ **أرقام {app} المتاحة حالياً:**\n\n"
        for n in nums[:12]: # عرض 12 رقم
            res_text += f"{icon} `{n}`\n"
        res_text += f"\n👨‍💻 بواسطة: {DEVELOPER_NAME}"
    else:
        res_text = f"💔 عذراً، هذه الدولة لا توجد لها أرقام حالياً.\n❤️‍🩹 **جرب دولة ثانية هي منزلت أرقام له.**"

    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"app_{app}"))
    bot.edit_message_text(res_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_home")
def back_home(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

bot.infinity_polling()
