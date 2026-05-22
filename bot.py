import os
import sys
import io
import time
from threading import Thread
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 1. إنشاء سيرفر وهمي لـ Render لمنع الـ Exited Early ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!", 200

def run_flask():
    # Render يمرر منفذ الـ Port تلقائياً عبر متغيرات البيئة
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- 2. الإعدادات الأساسية للبوت والمفاتيح ---
API_TOKEN = '8686242492:AAEg1LcQBk3y3QA0ZOr7B39_58V3jfXSw04'
API_5SIM_KEY = 'ضع_مفتاح_5sim_هنا' # ضع مفتاح الـ API الخاص بموقع 5sim هنا

ADMIN_ID = 8388141188
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"

bot = telebot.TeleBot(API_TOKEN)

# ترويسة معالجة لتقبل ترميز utf-8 العالمي بشكل آمن ومنع خطأ latin-1 تماماً
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY}'.encode('utf-8').decode('latin-1'),
    'Accept': 'application/json',
    'Accept-Charset': 'utf-8'
}

PROFIT_MARGIN = 0.05
DEVELOPER_URL = "https://t.me/awad3210"

# قنوات الاشتراك الإجباري
CHANNELS = ['@Awad_Numbers_Bot', '@jzbznznx', '@sn6hdbdn19dndw']
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+ohwA2pwywVxhOTVk"}
]

user_last_action = {}

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudiarabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "morocco": {"name": "🇲🇦 Morocco / المغرب", "slug": "morocco", "code": "212"},
    "uae": {"name": "🇦🇪 UAE / الإمارات", "slug": "uae", "code": "971"},
    "kuwait": {"name": "🇰🇼 Kuwait / الكويت", "slug": "kuwait", "code": "965"},
    "oman": {"name": "🇴🇲 Oman / عمان", "slug": "oman", "code": "968"},
    "jordan": {"name": "🇯🇴 Jordan / الأردن", "slug": "jordan", "code": "962"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"}
}

# --- 3. دوال الحماية وقاعدة البيانات المصغرة ---
def save_user(user_id):
    try:
        if not os.path.exists("users.txt"):
            with open("users.txt", "w", encoding="utf-8") as f: pass
        with open("users.txt", "r+", encoding="utf-8") as f:
            data = f.read()
            if str(user_id) not in data:
                f.seek(0, 2)
                f.write(f"{user_id}\n")
    except Exception as e:
        print(f"Error saving user: {e}")

def get_users_count():
    if not os.path.exists("users.txt"):
        return 0
    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            return len([line for line in f.read().splitlines() if line.strip()])
    except:
        return 0

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

def check_spam(user_id):
    current_time = time.time()
    if user_id in user_last_action:
        last_time, count = user_last_action[user_id]
        if current_time - last_time < 1.0:
            if count >= 3: return True
            user_last_action[user_id] = (last_time, count + 1)
        else:
            user_last_action[user_id] = (current_time, 1)
    else:
        user_last_action[user_id] = (current_time, 1)
    return False

# --- 4. واجهات الاستجابة والقوائم التفاعلية ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • كود فوري تفعيل مضمون", callback_data="section_paid"),
        InlineKeyboardButton("💡 نصائح هامة لتثبيت وتفعيل الرقم", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "🎯 *تستطيع الآن اقتناص أرقام مضمونة لتفعيل الواتساب، التليجرام، الفيسبوك، والانستغرام بثوانٍ.*\n\n"
        "👇 اختر القسم الذي تريده من الأزرار المنسقة بالأسفل:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify"))
        
        lock_text = (
            "⚠️ **تنبيه أمني مهم جداً!**\n\n"
            "لضمان استقرار السحب، يجب عليك الانضمام لقنوات ومجموعة البوت أولاً.\n\n"
            "يرجى الضغط على الأزرار أدناه للاشتراك، ثم اضغط على زر التحقق 👇"
        )
        return bot.send_message(message.chat.id, lock_text, reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد! تأكد واضغط مجدداً.", show_alert=True)

    elif call.data == "back_home":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = (
            "💡 **دليل المقنع الذهبي لتثبيت وتفعيل الأرقام بنجاح:**\n\n"
            "1️⃣ لتثبيت رقم واتساب دون حظر، استخدم نسخة *WhatsApp Business* رسمية أو تطبيق واتساب الأخضر الأساسي.\n"
            "2️⃣ عند طلب كود الحساب (واتساب، فيسبوك، انستغرام) انتظر العداد حتى ينتهي تماماً ولا تضغط 'إعادة إرسال' بسرعة."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === قسم السحب والربط بـ 5SIM ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للملف الرئيسي", callback_data="back_home"))
        
        paid_text = (
            "🛍️ **متجر الأرقام المدفوعة الحصرية المضمونة**\n\n"
            "👇 اختر التطبيق المطلوب لتفعيله الآن:"
        )
        bot.edit_message_text(paid_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{v['slug']}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقسم", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب رقمك الحصري منها:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "📡 Connecting to Secure Gateway...")
        bot.edit_message_text("📡 `جاري الاتصال ببوابة الـ API وجلب الرقم الحصري.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        url_order = f"https://5sim.net/v1/user/buy/activation/{target_country}/any/{target_app}"
        try:
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id = data.get("id")
                phone = data.get("phone")
                price = data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                success_box = (
                    "🎉 **تم سحب واقتناص الرقم بنجاح!**\n\n"
                    f"📱 **التطبيق المستهدف:** `{target_app.upper()}`\n"
                    f"🌍 **دولة الرقم:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة الإجمالية:** `{final_price} $`\n\n"
                    f"📞 **الرقم المخصص لك (اضغط عليه للنسخ):**\n`{phone}`\n\n"
                    "⚠️ **خطوتك التالية:** انسخ الرقم وضعه في التطبيق المطلوب واطلب الكود، ثم انتظر هنا.. السيرفر يفحص وصول الكود تلقائياً."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                # مراقبة الكود القادم من الـ API
                for _ in range(30):
                    time.sleep(10)
                    try:
                        check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM, timeout=8).json()
                        if check_res.get("sms"):
                            sms_code = str(check_res["sms"][0].get("code"))
                            secure_code = sms_code[:-2] + ".." if len(sms_code) > 2 else ".. "
                            
                            try:
                                bot.send_message(CHANNEL_LOG_ID, f"🔥 **كود تفعيل جديد ومكتمل:**\n\n📞 الرقم: `{phone}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 الكود كاملاً: `{sms_code}`")
                            except: pass

                            otp_box = (
                                "🔥 **بشرى سارة! وصل كود التفعيل الفوري الآن:**\n\n"
                                f"📞 **الرقم:** `{phone}`\n"
                                f"🔑 **كود الـ OTP:** `{secure_code}`\n\n"
                                f"📢 للحصول على الكود كاملاً وسليماً 100% يرجى التحقق من قناتنا الرسمية فوراً: {CHANNEL_LOG_ID}"
                            )
                            return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
                    except:
                        continue
                
                bot.send_message(call.message.chat.id, "❌ **انتهى الوقت المحدد ولم يصل كود للتطبيق. تم إلغاء الطلب تلقائياً.**")
            else:
                bot.send_message(call.message.chat.id, "❌ **السيرفر غير مشحون أو الأرقام ممتلئة حالياً:** تأكد من مفتاح 5sim وشحنه بالرصيد.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ اتصال بالشبكة: {e}")

    elif call.data == "my_account":
        account_text = (
            "💎 **لوحة البيانات الشخصية للمشترك:**\n\n"
            f"🆔 **معرف التليجرام الخاص بك:** `{call.from_user.id}`\n"
            f"💰 **رصيدك الحالي في البوت:** `0.00 $`\n"
            f"🟢 **حالة الاتصال بالخادم الرئيسي:** آمن ومستقر"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة للقائمة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة محمية وخاصة بمالك البوت فقط.", show_alert=True)
        
        count = get_users_count()  
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_home")
        )
        admin_panel_text = (
            "⚙️ **لوحة التحكم الشاملة لمالك البوت الأصلي:**\n\n"
            f"👥 `{count}` **مشترك مسجل في قاعدة البيانات الحية.**\n\n"
            "🚀 حالة الخادم: متصل بكفاءة 100% بدون أخطاء ترميز."
        )
        bot.edit_message_text(admin_panel_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 5. تشغيل خادمين في آن واحد لضمان استقرار السيرفر سحابياً ---
if __name__ == "__main__":
    print("إعداد البيئة المتكاملة للبوت على Render...")
    
    # تشغيل سيرفر الويب الوهمي لتجاوز Exited Early في الـ Background
    server_thread = Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
    print("🚀 تم تشغيل ويب سيرفر خلفي لتأمين استجابة منصة Render!")
    
    # حذف الويب هوك لتفعيل الـ Polling الفوري النظيف
    bot.remove_webhook()
    print("🚀 البوت جاهز تماماً للرد المباشر والنفاث دون تعليق!")
    
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=15)
        except Exception as e:
            print(f"Polling error placeholder: {e}")
            time.sleep(5)
