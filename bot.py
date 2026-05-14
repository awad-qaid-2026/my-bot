import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

# إعدادات البوت والقنوات
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
bot = telebot.TeleBot(API_TOKEN)
CHANNELS = ["@v_o_lti", "@jzbnznx", "@bsbsb8_djbd"]

# الـ 10 مواقع العالمية الشغالة 24 ساعة
SOURCES = [
    "https://receive-smss.com/", "https://sms-online.co/receive-free-sms",
    "https://receive-sms.cc/", "https://www.receivesms.co/",
    "https://smsreceivefree.com/", "https://getfreesmsnumber.com/",
    "https://temp-number.com/", "https://sms-receive.net/",
    "https://www.sms-arrival.com/", "https://fakesms.online/"
]

def is_subscribed(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except: return False

def fetch_mega_numbers():
    all_nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in SOURCES:
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for item in soup.find_all(['a', 'span', 'h4', 'p', 'td']):
                    txt = item.text.strip().replace(" ", "").replace("-", "")
                    if txt.startswith('+') and 10 < len(txt) < 16:
                        if txt not in all_nums: all_nums.append(txt)
            if len(all_nums) >= 40: break
        except: continue
    return all_nums

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        # تنسيق الأزرار مثل الصور التي أرفقتها
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_fb = types.InlineKeyboardButton("🔵 Facebook", callback_data="get_nums")
        btn_wa = types.InlineKeyboardButton("🟢 WhatsApp", callback_data="get_nums")
        btn_tg = types.InlineKeyboardButton("🔵 Telegram", callback_data="get_nums")
        btn_tt = types.InlineKeyboardButton("⚫ TikTok", callback_data="get_nums")
        btn_ig = types.InlineKeyboardButton("🟣 Instagram", callback_data="get_nums")
        
        markup.add(btn_fb, btn_wa, btn_tg, btn_tt, btn_ig)
        
        bot.send_message(message.chat.id, 
                         "⚔️ **Select a Service:**\n\n"
                         "أهلاً بك في بوت دمار المقنع.\n"
                         "اختر الخدمة التي تريد تفعيلها وسأجلب لك أرقاماً تعمل حالياً:", 
                         reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 انضم للقناة 1", url="https://t.me/v_o_lti"),
            types.InlineKeyboardButton("📢 انضم للقناة 2", url="https://t.me/jzbnznx"),
            types.InlineKeyboardButton("📢 انضم للقناة 3", url="https://t.me/bsbsb8_djbd"),
            types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="verify_it")
        )
        bot.send_message(message.chat.id, "⚠️ **يجب الاشتراك في القنوات أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "get_nums")
def handle_fetch(call):
    bot.answer_callback_query(call.id, "🔄 جاري فحص الأرقام المتاحة...")
    nums = fetch_mega_numbers()
    
    if nums:
        msg = "📲 **الأرقام المتوفرة لتفعيل خدمتك:**\n\n"
        for n in nums[:20]: # عرض 20 رقم لتجنب الزحام
            msg += f"• `{n}`\n"
        msg += "\n💡 *اضغط على الرقم لنسخه.* اطلب الكود وسيظهر في موقع الرقم."
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 تحديث القائمة", callback_data="get_nums"))
        markup.add(types.InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_start"))
        
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text("❌ لم أتمكن من جلب أرقام حالياً، حاول مرة أخرى.", call.message.chat.id, call.message.message_id, 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 محاولة أخرى", callback_data="get_nums")))

@bot.callback_query_handler(func=lambda call: call.data == "back_start")
def back_start(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "verify_it")
def verify_it(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التفعيل!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في القنوات أولاً!", show_alert=True)

bot.infinity_polling()
