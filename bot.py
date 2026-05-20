import sys, os, time, re, concurrent.futures
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import cloudscraper # يجب تثبيت هذه المكتبة
from bs4 import BeautifulSoup
from flask import Flask
from urllib.parse import quote

# --- 1. CONFIGURATION ---
API_TOKEN = '8686242492:AAHg-MIu67d9yPz0HhadvmSMdGclbunqyH4'
ADMIN_ID = 8388141188
bot = telebot.TeleBot(API_TOKEN)
scraper = cloudscraper.create_scraper()

# --- 2. 22+ COUNTRIES LIST ---
COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 اليمن", "slug": "yemen", "code": "967"},
    "usa": {"name": "🇺🇸 أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 بريطانيا", "slug": "united-kingdom", "code": "44"},
    "egypt": {"name": "🇪🇬 مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 العراق", "slug": "iraq", "code": "964"},
    "saudi": {"name": "🇸🇦 السعودية", "slug": "saudi-arabia", "code": "966"},
    "france": {"name": "🇫🇷 فرنسا", "slug": "france", "code": "33"},
    "germany": {"name": "🇩🇪 ألمانيا", "slug": "germany", "code": "49"},
    "russia": {"name": "🇷🇺 روسيا", "slug": "russia", "code": "7"},
    "sweden": {"name": "🇸🇪 السويد", "slug": "sweden", "code": "46"},
    "turkey": {"name": "🇹🇷 تركيا", "slug": "turkey", "code": "90"},
    "canada": {"name": "🇨🇦 كندا", "slug": "canada", "code": "1"},
    "india": {"name": "🇮🇳 الهند", "slug": "india", "code": "91"},
    "china": {"name": "🇨🇳 الصين", "slug": "china", "code": "86"},
    "morocco": {"name": "🇲🇦 المغرب", "slug": "morocco", "code": "212"},
    "uae": {"name": "🇦🇪 الإمارات", "slug": "united-arab-emirates", "code": "971"},
    "jordan": {"name": "🇯🇴 الأردن", "slug": "jordan", "code": "962"},
    "algeria": {"name": "🇩🇿 الجزائر", "slug": "algeria", "code": "213"},
    "tunisia": {"name": "🇹🇳 تونس", "slug": "tunisia", "code": "216"},
    "syria": {"name": "🇸🇾 سوريا", "slug": "syria", "code": "963"},
    "libya": {"name": "🇱🇾 ليبيا", "slug": "libya", "code": "218"},
    "palestine": {"name": "🇵🇸 فلسطين", "slug": "palestine", "code": "970"}
}

# --- 3. SCRAPER ENGINE (V2.0) ---
def scrape_single_source(url, code):
    nums = []
    try:
        r = scraper.get(url, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # البحث عن الأرقام بنمط +Code
            pattern = re.compile(rf"\+{code}\s?\d{{7,15}}")
            for text in soup.stripped_strings:
                match = pattern.search(text.replace(" ", ""))
                if match: nums.append(match.group())
    except: pass
    return list(set(nums))

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://anonymsms.com/country/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://sms24.me/en/countries/{slug}"
    ]
    all_numbers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_single_source, url, code) for url in sources]
        for f in concurrent.futures.as_completed(futures):
            all_numbers.extend(f.result())
    return list(set(all_numbers))[:12]

# --- 4. KEEP ALIVE (24/7) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

Thread(target=run).start()

# --- 5. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    for k, v in COUNTRIES_DATA.items():
        markup.add(InlineKeyboardButton(v["name"], callback_data=f"get_{k}"))
    bot.send_message(message.chat.id, "👑 **أهلاً بك في محرك المقنع النفاث**\nاختر الدولة لجلب الأرقام فوراً:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_"))
def get_numbers(call):
    country = call.data.split("_")[1]
    data = COUNTRIES_DATA[country]
    bot.answer_callback_query(call.id, "🚀 جاري فحص السيرفرات...")
    
    nums = fetch_all_sources_fast(data['code'], data['slug'])
    if nums:
        markup = InlineKeyboardMarkup(row_width=1)
        for n in nums: markup.add(InlineKeyboardButton(f"📞 {n}", callback_data="none"))
        bot.edit_message_text(f"✅ تم العثور على أرقام لـ {data['name']}:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ لا توجد أرقام متاحة حالياً، جرب دولة أخرى.", show_alert=True)

if __name__ == "__main__":
    bot.infinity_polling()
