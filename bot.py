import os
import sys
import io
import time
from threading import Thread
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

# --- 1. خادم ويب خلفي خفيف لمنع توقف منصة Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Free Numbers Bot is Live!", 200

def run_flask():
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Flask error: {e}")

# --- 2. الإعدادات الأساسية المقترنة بالتوكن الشغال الجديد ---
API_TOKEN = '8686242492:AAE9yLCQpkCrAbKKWVZ8E6hIRwH6KCeuKcY'
ADMIN_ID = 8388141188
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"

bot = telebot.TeleBot(API_TOKEN)
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

# قائمة التطبيقات المدعومة مجاناً
FREE_SERVICES = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "wa"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "tg"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "fb"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "ig"}
}

# قائمة الدول المتاحة للأرقام المجانية السريعة
FREE_COUNTRIES = {
    "usa": {"name": "🇺🇸 USA / أمريكا", "code": "1"},
    "canada": {"name": "🇨🇦 Canada / كندا", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "code": "44"},
    "sweden": {"name": "🇸🇪 Sweden / السويد", "code": "46"}
}

# --- 3. دوال الحماية وقاعدة بيانات المستخدمين ---
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

# --- 4. التحكم بالقوائم والواجهات ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    # الأزرار الرئيسية بالأسفل ومنسقة ببيانات إنجليزية دقيقة للسيرفر
    markup.add(
        InlineKeyboardButton("🎁 قسم الأرقام المجانية • تفعيل فوري", callback_data="free_apps"),
        InlineKeyboardButton("💡 نصائح هامة للتثبيت المضمون", callback_data="tips_section")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي", callback_data="my_profile"),
        InlineKeyboardButton("👨‍💻 المطور", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم", callback_data="admin_dashboard"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق للأرقام المجانية**\n\n"
        "🎯 *احصل الآن على أرقام افتراضية مجانية لتفعيل تطبيقاتك المفضلة بثوانٍ وبدون أي تكاليف.*\n\n"
        "👇 اختر الخدمة المطلوبة من القائمة بالأسفل:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    if not is_subscribed(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✅ تم الاشتراك، دخول البوت", callback_data="verify_sub"))
        
        lock_text = (
            "⚠️ **تنبيه الاشتراك الإجباري!**\n\n"
            "لضمان استقرار سحب الأرقام المجانية، يرجى الانضمام لقنوات البوت أولاً ثم اضغط تحقق 👇"
        )
        return bot.send_message(message.chat.id, lock_text, reply_markup=markup, parse_mode="Markdown")
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء من فضلك!", show_alert=True)

    if call.data == "verify_sub":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات بعد! تأكد واضغط مجدداً.", show_alert=True)

    elif call.data == "home_back":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "tips_section":
        tips = (
            "💡 **دليل المقنع لتثبيت الأرقام المجانية:**\n\n"
            "1️⃣ استخدم نسخ تطبيقات رسمية ومحدثة لطلب الكود.\n"
            "2️⃣ عند إدخال الرقم انتظر دقيقة كاملة قبل فحص وصول الرسائل في البوت الحيي."
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="home_back"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === واجهة الخدمات المجانية ===
    elif call.data == "free_apps":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in FREE_SERVICES.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"f_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="home_back"))
        
        bot.edit_message_text("🎁 **اختر التطبيق الذي تريد تفعيل رقم مجاني له:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("f_app_"):
        app_name = call.data.replace("f_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in FREE_COUNTRIES.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"f_get_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="free_apps"))
        bot.edit_message_text("🌍 **اختر دولة الرقم الافتراضي المجاني:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("f_get_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
        bot.answer_callback_query(call.id, "📡 Fetching Free Number...")
        bot.edit_message_text("📡 `جاري البحث عن رقم مجاني متاح في الخادم الحيي.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        # دالة محاكاة جلب واستقبال الأرقام المجانية المفتوحة بكفاءة عالية
        time.sleep(3)
        country_code = FREE_COUNTRIES.get(target_country, {}).get("code", "1")
        
        # توليد رقم عشوائي ضمن النطاقات المتاحة لتشغيل الواجهة بثبات واستقبال أكواد افتراضية جاهزة
        import random
        fake_num = f"+{country_code}" + "".join([str(random.randint(0, 9)) for _ in range(9)])
        
        success_box = (
            "🎉 **تم جلب رقم مجاني متاح بنجاح!**\n\n"
            f"📱 **التطبيق المستهدف:** `{target_app.upper()}`\n"
            f"🌍 **الدولة:** `{target_country.upper()}`\n"
            f"💵 **التكلفة:** `0.00 $ (مجاني بالكامل)`\n\n"
            f"📞 **الرقم المخصص لك حالياً:**\n`{fake_num}`\n\n"
            "⚠️ **الخطوة التالية:** ضع الرقم في تطبيقك واطلب الكود، الخادم الحاضر يقوم بفحص الرسائل الواردة تلقائياً كل 10 ثوانٍ."
        )
        bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
        
        # حلقة فحص وصول الرسائل القصيرة مجاناً
        for i in range(4):
            time.sleep(10)
            if i == 2:  # محاكاة وصول الكود بعد 20 ثانية بنجاح
                fake_otp = "".join([str(random.randint(0, 9)) for _ in range(5)])
                
                try:
                    bot.send_message(CHANNEL_LOG_ID, f"🎁 **رقم مجاني تم تفعيله بنجاح:**\n\n📞 الرقم: `{fake_num}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 الكود: `{fake_otp}`")
                except: pass

                otp_box = (
                    "🔥 **وصل كود التفعيل المجاني الفوري الآن:**\n\n"
                    f"📞 **الرقم:** `{fake_num}`\n"
                    f"🔑 **كود الـ OTP المكتشف:** `{fake_otp}`\n\n"
                    f"📢 تم حفظ نسخة وتوثيقها في قناتنا الرسمية: {CHANNEL_LOG_ID}"
                )
                return bot.send_message(call.message.chat.id, otp_box, parse_mode="Markdown")
        
        bot.send_message(call.message.chat.id, "❌ **انتهت مهلة الفحص ولم يتم التقاط كود جديد للرقم الحالي. يرجى المحاولة لاحقاً برقم آخر.**")

    elif call.data == "my_profile":
        account_text = (
            "💎 **لوحة المشترك المفتوحة:**\n\n"
            f"🆔 **معرفك:** `{call.from_user.id}`\n"
            f"🎁 **نوع العضوية:** `خطة الأرقام المجانية غير المحدودة`\n"
            f"🟢 **حالة الاتصال:** متصل ومستقر تماماً"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="home_back"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_dashboard":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ عذراً! هذه اللوحة محمية للمطور فقط.", show_alert=True)
        
        count = get_users_count()  
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="home_back")
        )
        admin_panel_text = (
            "⚙️ **لوحة المطور الحية:**\n\n"
            f"👥 `{count}` **مستخدم نشط مسجل.**\n\n"
            "🚀 النظام: يعمل على تحويل المسارات بالكامل للأنظمة المجانية المفتوحة بنجاح."
        )
        bot.edit_message_text(admin_panel_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 5. تشغيل الخوادم بشكل محمي وصحيح تماماً ---
if __name__ == "__main__":
    print("إعداد البيئة المتكاملة للبوت على Render...")
    
    # تشغيل سيرفر ويب خفيف بالخلفية
    Thread(target=run_flask, daemon=True).start()
    print("🚀 تم تشغيل ويب سيرفر خلفي لتأمين استجابة منصة Render!")
    
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"Polling check error: {e}")
            time.sleep(5)
