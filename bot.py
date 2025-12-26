import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# توکن ربات خودت (از BotFather)
TOKEN = '8512018392:AAFDwkoD-ACalyunTDeghXeQtoqoRqP3K58'  # توکن واقعی خودت رو بگذار

# آیدی کانال و گروه
CHANNEL_ID = '@PersianPwn'
GROUP_ID = '@PERSlANPWN'

# نام دقیق فایل اسکریپت (که کنار bot.py هست)
SCRIPT_FILE = 'nameless_hub.lua'  # اگر اسم فایلت فرق داره، اینجا تغییر بده

bot = telebot.TeleBot(TOKEN)

# تابع چک عضویت
def is_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except ApiTelegramException:
        return False

def check_membership(user_id):
    return is_member(user_id, CHANNEL_ID) and is_member(user_id, GROUP_ID)

# دستور /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_membership(user_id):
        send_script(message.chat.id)
    else:
        show_join_buttons(message.chat.id)

# دکمه چک عضویت
@bot.callback_query_handler(func=lambda call: call.data == 'check_join')
def check_join_callback(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.answer_callback_query(call.id, 'عضویت تأیید شد! فایل در حال ارسال...', show_alert=True)
        send_script(call.message.chat.id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    else:
        bot.answer_callback_query(call.id, 'هنوز عضو هر دو کانال و گروه نیستی! بعد از جوین شدن دوباره چک کن.', show_alert=True)

# نمایش دکمه‌های جوین
def show_join_buttons(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('📢 کانال اصلی', url='https://t.me/PersianPwn'))
    markup.add(types.InlineKeyboardButton('💬 گروه چت', url='https://t.me/PERSlANPWN'))
    markup.add(types.InlineKeyboardButton('✅ چک کردن عضویت', callback_data='check_join'))
    
    bot.send_message(chat_id,
                     '🎯 برای دریافت اسکریپت چیت، باید عضو کانال و گروه بشی!\n\n'
                     'بعد از عضویت در هر دو، روی دکمه زیر بزن 👇',
                     reply_markup=markup)

# ارسال فایل اسکریپت
def send_script(chat_id):
    try:
        with open(SCRIPT_FILE, 'rb') as file:
            bot.send_document(chat_id, file,
                              caption='🔥 اسکریپت چیت با موفقیت ارسال شد!\n'
                                      'لذت ببر و موفق باشی 😈\n'
                                      '@PersianPwn')
    except FileNotFoundError:
        bot.send_message(chat_id, '❌ فایل اسکریپت پیدا نشد! به ادمین اطلاع بده.')
    except Exception as e:
        bot.send_message(chat_id, '❌ خطایی در ارسال پیش آمد. دوباره امتحان کن.')

# دستور /check برای چک دوباره
@bot.message_handler(commands=['check'])
def check(message):
    start(message)

# شروع ربات با polling پایدار
print('ربات شروع شد و در حال اجراست...')

# این خط خیلی مهمه – ربات رو همیشه روشن نگه می‌داره
try:
    bot.infinity_polling(none_stop=True, interval=0, timeout=20)
except Exception as e:
    print(f'خطا رخ داد: {e} - دوباره تلاش می‌کنم...')
    import time
    time.sleep(5)
    bot.infinity_polling(none_stop=True)