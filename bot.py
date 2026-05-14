import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import concurrent.futures

# --- الإعدادات (عدلها بنفسك) ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
MY_CHANNELS = ['@dmar_almoqana']  # !!! ضع هنا معرف قناتك أنت فقط !!!
DEV_ID = "8388141188" # ايديك للتواصل
DEV_NAME = "اིلཻمຼقᮭن྄༹ع🎭"

bot = telebot.TeleBot(API_TOKEN)

# قائمة الـ 24 دولة مع الأكواد
COUNTRIES = {
    "1": "أمريكا 🇺🇸", "44": "بريطانيا 🇬🇧", "49": "ألمانيا 🇩🇪", "33": "فرنسا 🇫🇷",
    "7": "روسيا 🇷🇺", "46": "السويد 🇸🇪", "31": "هولندا 🇳🇱", "34": "إسبانيا 🇪🇸",
    "1787": "بورتوريكو 🇵🇷", "60": "ماليزيا 🇲🇾", "62": "إندونيسيا 🇮🇩", "63": "الفلبين 🇵🇭",
    "48": "بولندا 🇵🇱", "420": "التشيك 🇨🇿", "380": "أوكرانيا 🇺🇦", "40": "رومانيا 🇷🇴",
    "351": "البرتغال 🇵🇹", "32": "بلجيكا 🇧🇪", "41": "سويسرا 🇨🇭", "43": "النمسا 🇦🇹",
    "91": "الهند 🇮🇳", "86": "الصين 🇨🇳", "852": "هونج كونج 🇭🇰", "234": "نيجيريا 🇳🇬"
}

def is_sub(u_id):
    for ch in MY_CHANNELS:
        try:
            s = bot.get_chat_member(ch, u_id).status
            if s in ['left', 'kicked']: return False
        except: continue
    return True

def fetch_from_site(url, code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        nums = []
        for item in soup.find_all(['h4', 'a', 'span']):
            txt = item.text.strip().replace(" ", "")
            if txt.startswith(f'+{code}') and 10 < len(txt) < 16:
                if txt not in nums: nums.append(txt)
        return nums
    except: return []

def get_all_numbers(code):
    urls = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://sms-online.co/receive-free-sms/{code}",
        f"https://receive-sms.cc/Free-SMS-Number/{code}"
    ]
    all_n = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(lambda u: fetch_from_site(u, code), urls)
        for res in results: all_n.extend(res)
    return list(set(all_n))[:12] # إرجاع 12 رقم مميز

@bot.message_handler(commands=['start'])
def start(message):
    if not is_sub(message.from_user.id):
        m = types.InlineKeyboardMarkup(row_width=1)
        for ch in MY_CHANNELS:
            m.add(types.InlineKeyboardButton("📢 اشترك في قناة البوت", url=f"https://t.me/{ch.replace('@','')}"))
        m.add(types.InlineKeyboardButton("✅ تم الاشتراك", callback_data="check"))
        bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القناة لفتح البوت:**", reply_markup=m)
    else:
        main_menu(message.chat.id)

def main_menu(cid):
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(
        types.InlineKeyboardButton("🟢 WhatsApp", callback_data="svc_WA_🟢"),
        types.InlineKeyboardButton("🔵 Facebook", callback_data="svc_FB_👤"),
        types.InlineKeyboardButton("✈️ Telegram", callback_data="svc_TG_✈️"),
        types.InlineKeyboardButton("📸 Instagram", callback_data="svc_IG_📸"),
        types.InlineKeyboardButton("🎵 TikTok", callback_data="svc_TK_🎵"),
        types.InlineKeyboardButton(f"👨‍💻 تواصل مع المطور {DEV_NAME}", url=f"tg://user?id={DEV_ID}")
    )
    bot.send_message(cid, f"⚔️ **أهلاً بك في بوت {DEV_NAME}**\nاختر الخدمة:", reply_markup=m, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: True)
def calls(c):
    if c.data == "check":
        if is_sub(c.from_user.id):
            bot.delete_message(c.message.chat.id, c.message.message_id)
            main_menu(c.message.chat.id)
        else: bot.answer_callback_query(c.id, "❌ اشترك أولاً!", show_alert=True)

    elif c.data.startswith("svc_"):
        _, svc, ico = c.data.split("_")
        m = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(name, callback_data=f"get_{svc}_{code}_{ico}") for code, name in COUNTRIES.items()]
        m.add(*btns)
        m.add(types.InlineKeyboardButton("🔙 عودة", callback_data="home"))
        bot.edit_message_text(f"📍 **الخدمة:** {svc}\nاختر الدولة:", c.message.chat.id, c.message.message_id, reply_markup=m)

    elif c.data.startswith("get_"):
        _, svc, code, ico = c.data.split("_")
        bot.answer_callback_query(c.id, "🔍 جاري سحب الأرقام من كافة المواقع...")
        nums = get_all_numbers(code)
        if nums:
            m = types.InlineKeyboardMarkup(row_width=1)
            for n in nums: m.add(types.InlineKeyboardButton(f"{ico} {n}", callback_data="copy"))
            m.add(types.InlineKeyboardButton("🔙 عودة للدول", callback_data=f"svc_{svc}_{ico}"))
            bot.edit_message_text(f"✅ **أرقام {svc} المتاحة ({COUNTRIES[code]}):**", c.message.chat.id, c.message.message_id, reply_markup=m)
        else: bot.answer_callback_query(c.id, "❌ لا توجد أرقام حالياً، جرب دولة أخرى", show_alert=True)

    elif c.data == "home":
        bot.delete_message(c.message.chat.id, c.message.message_id)
        main_menu(c.message.chat.id)
    
    elif c.data == "copy":
        bot.answer_callback_query(c.id, "تم اختيار الرقم! انسخه وجربه الآن.", show_alert=True)

bot.infinity_polling()
