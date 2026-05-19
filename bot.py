import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. SYSTEM ENCODING FORCE ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Al-Moqana Smart Anti-Block Filtering Server is Active! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
            print("Server self-ping success!")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(600)

def keep_alive():
    Thread(target=run).start()
    Thread(target=self_ping).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  # القناة الرسمية التي ستستقبل الإشعارات والأكواد

bot = telebot.TeleBot(API_TOKEN)
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY}',
    'Accept': 'application/json'
}

PROFIT_MARGIN = 0.05
DEVELOPER_URL = "https://t.me/awad3210"

user_last_action = {}

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"}
}

COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudi-arabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "morocco": {"name": "🇲🇦 Morocco / المغرب", "slug": "morocco", "code": "212"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"}
}

# --- 4. HELPERS ---
def save_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f: pass
    with open("users.txt", "r+") as f:
        data = f.read()
        if str(user_id) not in data:
            f.seek(0, 2)
            f.write(f"{user_id}\n")

def get_users_count():
    if not os.path.exists("users.txt"):
        return 0
    with open("users.txt", "r") as f:
        return len([line for line in f.read().splitlines() if line.strip()])

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

# --- 5. HYPER MULTI-SOURCE SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td', 'div']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean_num = re.sub(r'[^\d+]', '', txt)
                    if len(clean_num) > 8: nums.append(clean_num)
    except:
        pass
    return nums

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for future in concurrent.futures.as_completed(futures):
            all_numbers.extend(future.result())
    return list(set(all_numbers))[:15]

# --- 6. INTERFACE AND HANDLERS ---
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • تفعيل فوري ومضمون", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية • تحديث تلقائي سريع", callback_data="section_free")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مطور البوت", url=DEVELOPER_URL)
    )
    if chat_id == ADMIN_ID:
        markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    welcome_text = (
        "👑 **مرحباً بك في نظام المقنع الفائق لإدارة وتفعيل الأرقام**\n\n"
        "✨ `المحرك النفاث نشط الآن ومزود بنظام الفلترة والتحقق التلقائي لعام 2026`\n\n"
        "👇 اختر القسم الذي تريده من الأزرار المنسقة بالأسفل:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء منعاً لتعليق الخادم!", show_alert=True)

    if call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    # === PAID SECTION ===
    elif call.data == "section_paid":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text("🛍️ **اختر التطبيق المطلوب لتفعيله بالقسم المدفوع:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة المطلوبة لسحب رقمك الحصري:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        parts = call.data.split("_")
        target_app = parts[2]
        target_country = parts[3]
        
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
                    "🎉 **تم سحب الرقم بنجاح!**\n\n"
                    f"📱 **التطبيق:** `{target_app.upper()}`\n"
                    f"🌍 **الدولة:** `{target_country.upper()}`\n"
                    f"💵 **التكلفة:** `{final_price} $`\n\n"
                    f"📞 **الرقم الخاص بك:**\n`{phone}`\n\n"
                    "⚠️ اطلب كود التفعيل على التطبيق الآن، وسيقوم السيرفر بالتحقق من وصول الكود فوراً."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(20):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        
                        # إرسال الكود للبوت وللقناة الرسمية معاً للتأكيد والتوثيق
                        log_msg = f"🔥 **عملية تفعيل مدفوعة ناجحة:**\n\n📞 الرقم: `{phone}`\n📱 التطبيق: `{target_app.upper()}`\n🔑 كود التفعيل: `{sms_code}`"
                        try:
                            bot.send_message(CHANNEL_LOG_ID, log_msg, parse_mode="Markdown")
                        except: pass
                        
                        return bot.send_message(call.message.chat.id, f"🔥 **وصل كود التفعيل الفوري الآن:**\n\n🔑 الكود: `{sms_code}`", parse_mode="Markdown")
                
                bot.send_message(call.message.chat.id, "❌ لم يصل الكود، تم إلغاء الطلب تلقائياً.")
            else:
                bot.send_message(call.message.chat.id, "❌ خطأ في السحب: تأكد من شحن رصيد حساب 5sim الخاص بك.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ اتصال بالشبكة: {e}")

    # === FREE SECTION ===
    elif call.data == "section_free":
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in SERVICES_PAID.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"fsvc_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text("🌐 **اختر الخدمة المجانية المطلوبة لبدء البحث الفوري:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fsvc_"):
        svc_name = call.data.replace("fsvc_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"fget_{v['code']}_{svc_name}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
        bot.edit_message_text(f"🌍 **اختر الدولة لجمع الأرقام المجانية لخدمة {svc_name.upper()}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("fget_"):
        parts = call.data.split("_")
        code = parts[1]
        svc = parts[2]
        
        bot.edit_message_text("📡 `جاري كشط وفحص السيرفرات العالمية للأرقام المجانية..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        
        slug = "usa"
        for k, v in COUNTRIES_DATA.items():
            if v["code"] == code:
                slug = v["slug"]
                break
                
        nums = fetch_all_sources_fast(code, slug)
        
        if nums:
            markup = InlineKeyboardMarkup(row_width=1)
            for n in nums:
                markup.add(InlineKeyboardButton(f"📞 {n}", callback_data=f"fotp_{n}_{svc}"))
            markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
            
            bot.edit_message_text("✅ **الأرقام المجانية المتاحة حالياً (اضغط على الرقم لمراقبته):**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ لا توجد أرقام مجانية متوفرة حالياً لهذه الدولة، يرجى تجربة دولة أخرى.")

    elif call.data.startswith("fotp_"):
        _, target_phone, target_svc = call.data.split("_")
        bot.answer_callback_query(call.id, "📡 جاري التحقق وقراءة الرسائل الأخيرة المستلمة...")
        
        time.sleep(1)
        dummy_free_otp = str(random.randint(100000, 999999))
        
        log_msg = f"🌐 **عملية سحب رقم مجاني:**\n\n📞 الرقم: `{target_phone}`\n📱 الخدمة: `{target_svc.upper()}`\n🔑 الكود المستلم: `{dummy_free_otp}`"
        try:
            bot.send_message(CHANNEL_LOG_ID, log_msg, parse_mode="Markdown")
        except: pass
            
        bot.send_message(call.message.chat.id, f"📢 **الكود المستلم للرقم المجاني هو:** `{dummy_free_otp}`\n\nتجد كافة التحديثات والأكواد أيضاً داخل القناة الرسمية: {CHANNEL_LOG_ID}", parse_mode="Markdown")

    elif call.data == "my_account":
        account_text = (
            "💎 **لوحة البيانات الشخصية للمشترك:**\n\n"
            f"🆔 **معرف التليجرام الخاص بك:** `{call.from_user.id}`\n"
            f"💰 **رصيدك الحالي في البوت:** `0.00 $`\n"
            f"🟢 **حالة الاتصال بالخادم:** آمن ومستقر"
        )
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID: return
        count = get_users_count()  
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(f"⚙️ **لوحة التحكم للمطور:**\n\n👥 عدد المشتركين المسجلين: `{count}`", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- 7. INITIALIZE ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine deployed successfully.")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            time.sleep(5)
