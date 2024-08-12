import email
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import re
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from telebot import types
import os
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import schedule
import schedule
import sys
import time
from fuzzywuzzy import process

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '7423793308:AAFlo_yazQxHhq1MB8kNNpjpVIQSoDLdMdk'
CHANNEL_CHAT_ID = '@xhebtksoxkammtoscknwpgkcxbbag'
IMAGE_DIR = 'transaction_images'
ALLOWED_CHAT_ID = 6346924674
ALLOWED_CHAT_ID = -1002000759334

bot = telebot.TeleBot(TOKEN)

# الدالة التي ستقوم بإعادة المحاولة عند فشل إرسال الرسالة
def send_message_with_retry(bot, chat_id, text):
    max_retries = 3
    retry_delay = 30  # الوقت الذي سيتم الانتظار فيه بين المحاولات بالثواني

    for attempt in range(max_retries):
        try:
            bot.send_message(chat_id, text)
            print("Message sent successfully!")
            return
        except telebot.apihelper.ApiException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Failed to send message after multiple attempts.")

# دالة إرسال الرسائل للقناة مع إعادة المحاولة
def send_message_to_channel(text):
    send_message_with_retry(bot, CHANNEL_CHAT_ID, text)

# دالة إرسال الصور للقناة
def send_photo_to_channel(photo_path, caption=""):
    with open(photo_path, 'rb') as photo:
        bot.send_photo(CHANNEL_CHAT_ID, photo, caption=caption)

# تحقق من وجود مجلد الصور وإنشائه إذا لم يكن موجوداً
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
#--------------------------------------------------------------------------------------------------

#بنود وشروط الاستخدام
TERMS_AND_CONDITIONS = """
بنود وشروط الاستخدام

1. مدة الاستثمار والعوائد:

لدينا أربع خيارات استثمارية:

الخيار الأول: استثمار لمدة شهر بعائد 30%.

الخيار الثاني: استثمار لمدة ثلاثة أشهر بعائد 90%.

الخيار الثالث: استثمار لمدة ستة أشهر بعائد 180%.

الخيار الرابع: استثمار لمدة سنة بعائد 400%.

لا يمكنك سحب الأموال قبل تاريخ انتهاء فترة الاستثمار المختارة.

2. الاستثمار المتعدد:
إذا كنت قد استثمرت من قبل وكان استثمارك سارياً، وترغب في الاستثمار مرة أخرى، فسيكون استثماراً منفصلاً بربح محدد ووقت محدد لا علاقة له بالاستثمار الأول.

3. تغيير كلمة المرور:
عند فقدان كلمة المرور الخاصة بك، يمكنك تغييرها من خلال الإعدادات. إذا فقدت إمكانية الوصول إلى حسابك وتواصلت مع فريق الدعم، سيتم إرسال رمز التحقق إلى بريدك الإلكتروني للتحقق من أنك مالك الحساب.

4. تغيير البريد الإلكتروني:
إذا فقدت صلاحيات الوصول إلى بريدك الإلكتروني الذي قمت بالتسجيل به، يمكنك تغييره من خلال الإعدادات. إذا فقدت صلاحيات الوصول إليه، قم بالتواصل مع فريق الدعم في أقرب وقت ممكن للحصول على المساعدة في تغيير البريد الإلكتروني واستعادة الوصول إلى حسابك.

5. مشاركة المعلومات:
نحن لسنا مسؤولين إذا قمت بمشاركة معلوماتك مع أي شخص أو تسريب معلومات تسجيل الدخول الخاصة بك إلى أي شخص وقام بتصفية رصيدك أو القيام بأي عملية غير مصرح بها.

6. التحقق من العمليات المالية:
يتم التحقق من عملية السحب أو الإيداع خلال فترة تتراوح من ساعة إلى 24 ساعة.

7. فقدان الوصول للحساب:
نحن لسنا مسؤولين إذا فقدت الوصول إلى حسابك ولم تقدم طلبا لتغيير البريد الإلكتروني أو لم تقم بإدخال المعلومات الأساسية. ويأتي هذا القرار بسبب عدم وجود طرق أخرى للتحقق من أنك مالك الحساب

8. خيارات الاستثمار:
نستثمر لكم حالياً في الصناديق الاستثمارية التي نديرها بالعملات الرقمية

9. طرق الإيداع والسحب:
نتلقى الأموال عبر عملة USDT أو بنك الكريمي أو بنك الراجحي و خياراتنا لسحب الأموال هي عبر عبر USDT أو بنك كريمي، ونطمح مستقبلاً إلى توسيع خيارات السحب والإيداع بشكل أكبر

10. الحد الأدنى للسحب والاستثمار والإيداع:
الحد الأدنى للسحب هو 20 دولارًا والحد الأدنى للاستثمار هو 30 دولارًا والحد الأدنى للإيداع هو 30 دولارًا.


11. الاستخدام الرسمي:
إن الطريقة الرسمية الوحيدة للاستثمار والسحب والإيداع والوظائف الأخرى هي عبر البوت الخاص بنا. يجب على المستخدمين اتباع التعليمات الموجودة في البوت لتنفيذ العمليات.
نحن لا نقوم أبداً بتحويل المستخدمين إلى طرف ثالث لأي غرض. يُنصح المستخدمون بالحذر من أي عمليات احتيالية.

12. مسؤولية المستخدم:
نحن لا نتحمل أي مسؤولية إذا قام المستخدم بتنفيذ عمليات الإيداع أو السحب عن طريق أي طرف ثالث غير معتمد.

13. استخدام الهويات الزائفة:
يُمنع تماماً إنشاء حسابات جديدة باستخدام هويات زائفة. في حال اكتشاف أي حساب يستخدم هوية زائفة، سيتم حظر الحساب فوراً دون سابق إنذار.

14. حماية معلومات المستخدمين:
نحن نلتزم بحماية معلومات المستخدمين بشكل كامل. يتم التعامل مع جميع بيانات المستخدمين بسرية تامة وفقًا لسياسة الخصوصية المعتمدة لدينا.
لا نتحمل أي مسؤولية في حال قام المستخدم بمشاركة معلومات تسجيل الدخول الخاصة به مع أي طرف ثالث. يجب على المستخدمين الحفاظ على سرية معلوماتهم وعدم مشاركتها مع أي شخص آخر.

15. غسل الأموال:
يُمنع منعاً باتاً استخدام نظام الإيداع الخاص بنا لغرض غسل الأموال. يتم مراقبة جميع العمليات المالية والتبليغ عن أي نشاط مريب إلى السلطات المختصة.
في حال اكتشاف أي نشاط يتعلق بغسل الأموال، سيتم حظر الحساب فوراً وإبلاغ الجهات المختصة لاتخاذ الإجراءات القانونية اللازمة.

16. فريق الدعم:
فريق الدعم لا يقوم بأي حال من الأحوال بمراسلتك أولاً أو عبر طرق غير مذكورة في البوت. يجب على المستخدمين التواصل مع فريق الدعم عبر القنوات الرسمية المصرح بها فقط.

17. متطلبات سحب الأموال
لا يمكنك سحب الأموال من غير إتمام عملية استثمار واحدة على الأقل. يجب عليك إتمام عملية استثمار واحدة لتكون مؤهلاً لسحب الأموال.

18. إخلاء المسؤولية:
يُنصح المستخدمون بالتحقق من التعليمات الرسمية والإجراءات المتبعة في البوت لتجنب أي التباس أو خطأ قد يؤدي إلى فقدان الأموال أو أي مشكلة أخرى.

19. تطبيق القوانين والشروط:
يحق لنا تطبيق أي قوانين أو شروط غير مذكورة في هذه الوثيقة إذا دعت الحاجة لذلك من أجل حماية النظام والمستخدمين.


عند قيامك بإنشاء حساب جديد، فإنك توافق على شروط وأحكام الاستخدام الخاصة بنا.
"""
#--------------------------------------------------------------------------------------------------

#قاعده البيانات
ACCOUNTS_FILE_PATH = 'accounts.txt'
LOGGED_IN_USERS_FILE_PATH = 'logged_in_users.txt'
BANNED_ACCOUNTS_FILE_PATH = 'banned_accounts.txt'
NOTIFICATIONS_FILE_PATH = 'notifications.txt'
INVESTOR_EMAILS_FILE_PATH = 'investor_emails.txt'
TELEGRAM_IDS_FILE_PATH = 'telegram_ids.txt'
# قاعدة البيانات المؤقتة
accounts = {}
logged_in_users = {}
banned_accounts = {}
notifications = {}
telegram_ids = {}
# تحميل الحسابات من ملف النص
def load_accounts():
    global accounts
    try:
        with open(ACCOUNTS_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    email, password, fullname, balance = line.strip().split(', ')
                    accounts[email] = {
                        'password': password,
                        'fullname': fullname,
                        'balance': float(balance)
                    }
    except FileNotFoundError:
        pass

# حفظ الحسابات في ملف النص
def save_accounts():
    with open(ACCOUNTS_FILE_PATH, 'w', encoding='utf-8') as file:
        for email, info in accounts.items():
            file.write(f"{email}, {info['password']}, {info['fullname']}, {info['balance']}\n")

# تحميل المستخدمين المسجلين من ملف النص
def load_logged_in_users():
    global logged_in_users
    logged_in_users = {}
    try:
        with open(LOGGED_IN_USERS_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    chat_id, email = line.strip().split(', ')
                    logged_in_users[int(chat_id)] = email
    except FileNotFoundError:
        pass
    return logged_in_users

# حفظ المستخدمين المسجلين في ملف النص
def save_logged_in_users(logged_in_users):
    with open(LOGGED_IN_USERS_FILE_PATH, 'w', encoding='utf-8') as file:
        for chat_id, email in logged_in_users.items():
            file.write(f"{chat_id}, {email}\n")

# تحميل الحسابات المحظورة من ملف النص
def load_banned_accounts():
    global banned_accounts
    banned_accounts = {}
    try:
        with open(BANNED_ACCOUNTS_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    email, reason = line.strip().split(', ')
                    banned_accounts[email] = reason
    except FileNotFoundError:
        pass
    return banned_accounts

# حفظ الحسابات المحظورة في ملف النص
def save_banned_accounts(banned_accounts):
    with open(BANNED_ACCOUNTS_FILE_PATH, 'w', encoding='utf-8') as file:
        for email, reason in banned_accounts.items():
            file.write(f"{email}, {reason}\n")

# تحديث حالة تسجيل الدخول
def update_logged_in_users(email, action):
    try:
        with open(LOGGED_IN_USERS_FILE_PATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(LOGGED_IN_USERS_FILE_PATH, 'w', encoding='utf-8') as file:
            for line in lines:
                if email not in line:
                    file.write(line)
        if action == 'add':
            chat_id = next((k for k, v in logged_in_users.items() if v == email), None)
            if chat_id:
                logged_in_users[chat_id] = email
                save_logged_in_users(logged_in_users)
    except FileNotFoundError:
        pass

# تغيير البريد الإلكتروني في قاعدة البيانات
def change_email_in_db(current_email, new_email):
    if current_email in accounts:
        if new_email in accounts:
            return False, "عذراً، هذا الحساب مستخدم من قبل. يرجى إدخال بريد إلكتروني آخر."

        # حذف البريد الإلكتروني القديم من ملف logged_in_users
        update_logged_in_users(current_email, 'remove')

        # تغيير البريد الإلكتروني في قاعدة البيانات
        accounts[new_email] = accounts.pop(current_email)
        save_accounts()
        return True, None
    return False, "البريد الإلكتروني الحالي غير موجود في النظام."

# تغيير كلمة المرور في قاعدة البيانات
def change_password_in_db(email, new_password):
    if email in accounts:
        accounts[email]['password'] = new_password
        save_accounts()
        return True
    return False

# تحميل الإشعارات من ملف النص
def load_notifications():
    global notifications
    notifications = {}
    try:
        with open(NOTIFICATIONS_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(', ', 3)
                    if len(parts) == 4:
                        email, title, body, date = parts
                        if email not in notifications:
                            notifications[email] = []
                        notifications[email].append({'title': title, 'body': body, 'date': date})
    except FileNotFoundError:
        pass

# إضافة إشعار للمستخدم
def add_notification(email, title, body):
    if email in accounts:  # تأكد من تعريف accounts بشكل صحيح
        if email not in notifications:
            notifications[email] = []
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notifications[email].append({'title': title, 'body': body, 'date': date})
        save_notifications()

# حفظ الإشعارات في ملف النص
def save_notifications():
    try:
        with open(NOTIFICATIONS_FILE_PATH, 'w', encoding='utf-8') as file:
            for email, user_notifications in notifications.items():
                for notification in user_notifications:
                    file.write(f"{email}, {notification['title']}, {notification['body']}, {notification['date']}\n")
    except Exception as e:
        print(f"Error saving notifications: {e}")


# تسجيل خروج الجلسات السابقة للمستخدم
def logout_other_sessions(email):
    global logged_in_users
    sessions_to_remove = [chat_id for chat_id, user_email in logged_in_users.items() if user_email == email]
    for chat_id in sessions_to_remove:
        logged_in_users.pop(chat_id, None)
    save_logged_in_users(logged_in_users)

#معرفات انشاء حساب جديد
def load_telegram_ids():
    global telegram_ids
    if not os.path.exists(TELEGRAM_IDS_FILE_PATH):
        telegram_ids = {}
    else:
        with open(TELEGRAM_IDS_FILE_PATH, 'r', encoding='utf-8') as file:
            telegram_ids = {line.strip().split(', ')[0]: (line.strip().split(', ')[1], line.strip().split(', ')[2]) for line in file}

def save_investor_email(email):
    with open(INVESTOR_EMAILS_FILE_PATH, 'a') as file:
        file.write(email + '\n')

# دالة للتحقق من وجود البريد الإلكتروني في ملف المستثمرين
def has_invested_before(email):
    try:
        with open(INVESTOR_EMAILS_FILE_PATH, 'r') as file:
            emails = file.readlines()
            emails = [e.strip() for e in emails]
            return email in emails
    except FileNotFoundError:
        return False

# تحميل البيانات عند بدء التشغيل
load_accounts()
logged_in_users = load_logged_in_users()
banned_accounts = load_banned_accounts()
load_notifications()
load_telegram_ids()
load_notifications()

#--------------------------------------------------------------------------------------------------

#ازرار البوت الرئيسيه

#تسجيل الدخول
def create_start_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_register = KeyboardButton('إنشاء حساب')
    btn_login = KeyboardButton('تسجيل الدخول')
    btn_terms = KeyboardButton('شروط الاستخدام')

    keyboard.add(btn_register, btn_login, btn_terms)

    return keyboard

#-----------------------

#القائمه الرئيسيه

def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn_invest = KeyboardButton('استثمار')
    btn_deposit = KeyboardButton('إيداع')
    btn_withdraw = KeyboardButton('سحب')
    btn_account_info = KeyboardButton('عرض الحساب')
    btn_terms = KeyboardButton('الاشعارات')
    btn_settings = KeyboardButton('إعدادات')
    help_button= KeyboardButton('المساعدة')

    keyboard.add(btn_invest)
    keyboard.add(btn_deposit, btn_withdraw)
    keyboard.add(btn_account_info)
    keyboard.add(btn_terms, btn_settings)
    keyboard.add(help_button)

    return keyboard

#-----------------------

#زر الرجوع
def create_back_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_back = KeyboardButton('رجوع')
    keyboard.add(btn_back)
    return keyboard


def handle_back_button(message):
    main_keyboard = create_main_keyboard()
    bot.send_message(message.chat.id, "العودة إلى القائمة الرئيسية", reply_markup=main_keyboard)


@bot.message_handler(func=lambda message: message.text == 'رجوع')
def handle_back(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    handle_back_button(message)

#-----------------------

# ازرار الاستثمار
def create_investment_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_invest_30 = KeyboardButton('شهر بعائد 30%')
    btn_invest_90 = KeyboardButton('ثلاثة أشهر بعائد 90%')
    btn_invest_180 = KeyboardButton('ستة أشهر بعائد 180%')
    btn_invest_400 = KeyboardButton('سنة بعائد 400%')
    btn_back = KeyboardButton('رجوع')
    keyboard.add(btn_invest_30, btn_invest_90, btn_invest_180, btn_invest_400, btn_back)
    return keyboard

#-----------------------

#ازرار الاعدادات
def create_settings_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


    btn_devices = KeyboardButton('الأجهزة المرتبطة')
    btn_change_password = KeyboardButton('تغيير كلمة المرور')
    btn_change_email = KeyboardButton('تغيير البريد الإلكتروني')
    btn_logout = KeyboardButton('تسجيل الخروج')
    btn_transfer = KeyboardButton('تحويل المال')
    btn_terms = KeyboardButton('شروط الاستخدام')
    btn_back = KeyboardButton('رجوع')


    keyboard.add(btn_devices)
    keyboard.add(btn_change_email, btn_change_password)
    keyboard.add(btn_logout)
    keyboard.add(btn_transfer, btn_terms)
    keyboard.add(btn_back)

    return keyboard

#-----------------------

# ازرار الايداع
def create_deposit_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_usdt = KeyboardButton('USDT (TRC20)')
    btn_kuraimi = KeyboardButton('بنك الكريمي')
    btn_rajhi = KeyboardButton('بنك الراجحي')
    Western_Union  = KeyboardButton('ويسترن يونيون')
    btn_back = KeyboardButton('رجوع')
    keyboard.add(btn_usdt, btn_kuraimi, btn_rajhi, Western_Union, btn_back )
    return keyboard

#-----------------------

# ازرار السحب
def create_withdraw_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_usdt = KeyboardButton('USDT (TRC20).')
    btn_kuraimi = KeyboardButton('بنك الكريمي.')
    Western_Union  = KeyboardButton('ويسترن يونيون')
    btn_back = KeyboardButton('رجوع')
    keyboard.add(btn_usdt, btn_kuraimi, Western_Union, btn_back )
    return keyboard

#--------------------------------------------------------------------------------------------------

#ازرار الادمن


#ازرار القائمه الرئيسيه للادمن
def create_saher_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    lll = KeyboardButton('باند')
    mmm = KeyboardButton('رصيد')
    ppp = KeyboardButton('ارسال الاشعارات')
    keyboard.add(mmm, lll, ppp)

    return keyboard

#-----------------------

#ازرار الباند
def create_saher1_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bbb = KeyboardButton('إلغاء حظر مستخدم')
    zzz = KeyboardButton('حظر مستخدم')
    aaa = KeyboardButton('ازرار التحكم')
    keyboard.add(zzz, bbb, aaa)

    return keyboard

#-----------------------

#ازرار الرصيد
def create_saher2_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    ewq = KeyboardButton('إرسال')
    qwe = KeyboardButton('خصم')
    wqe = KeyboardButton('ازرار التحكم')
    keyboard.add(qwe, ewq, wqe)

    return keyboard

#-----------------------

#ازرار الاشعارات
def create_saher3_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    mnb = KeyboardButton('إشعار للجميع')
    bnm = KeyboardButton('إشعار لمستخدم')
    lmn = KeyboardButton('ازرار التحكم')
    keyboard.add(mnb, bnm, lmn)

    return keyboard

# ازرار الدعم الفني
#--------------------------------------------------------------------------------------------------

#ارسال كود تحقق
def send_verification_email(email, code):
    sender_email = "invest_pioneers@hotmail.com"
    sender_password = "Aa223300"
    msg = MIMEText(f"كود التحقق الخاص بك على منصة رواد الاستثمار هو: {code}")
    msg['Subject'] = 'كود التحقق'
    msg['From'] = sender_email
    msg['To'] = email

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def generate_verification_code():
    return random.randint(100000, 999999)

#--------------------------------------------------------------------------------------------------

#معرفات الازرار والازرار الصغيره


#تسجيل الخروج
@bot.message_handler(func=lambda message: message.text == 'تسجيل الخروج')
def request_logout_confirmation(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول.", reply_markup=create_start_keyboard())
        return

    bot.send_message(message.chat.id, "• هل أنت متأكد من أنك تريد تسجيل الخروج؟", reply_markup=create_confirm_cancelK_keyboard())
    bot.register_next_step_handler(message, confirm_logout)

def confirm_logout(message):
    if message.text == 'تأكيد':
        if message.chat.id in logged_in_users:
            del logged_in_users[message.chat.id]
            save_logged_in_users(logged_in_users)
            bot.send_message(message.chat.id, "• لقد تم تسجيل خروجك بنجاح.", reply_markup=create_start_keyboard())
        else:
            bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول.", reply_markup=create_start_keyboard())
    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية تسجيل الخروج.", reply_markup=create_main_keyboard())
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_logout)

#-----------------------

#شروط الاستخدام
@bot.message_handler(func=lambda message: message.text == 'شروط الاستخدام')
def show_terms(message):
    bot.send_message(message.chat.id, TERMS_AND_CONDITIONS)

#-----------------------

#استثمار
@bot.message_handler(func=lambda message: message.text == 'استثمار')
def show_investment_options(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "اختر خطة الاستثمار:", reply_markup=create_investment_keyboard())

#-----------------------

#ايداع
@bot.message_handler(func=lambda message: message.text == 'إيداع')
def show_deposit_options(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "اختر طريقة الإيداع:", reply_markup=create_deposit_keyboard())

#-----------------------

# عرض الحساب
@bot.message_handler(func=lambda message: message.text == 'عرض الحساب')
def display_account_info(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    email = logged_in_users[message.chat.id]
    account = accounts[email]
    bot.send_message(message.chat.id, f"• معلومات الحساب:\n  \nالاسم الرباعي: {account['fullname']}\nالبريد الإلكتروني: {email}\nالرصيد: {account['balance']}$")

#-----------------------

#التحويل الا الاداره
@bot.message_handler(func=lambda message: message.text.lower() == 'ساهر حولني للاداره')
def send_saher_keyboard(message):
    markup = create_saher_keyboard()
    bot.send_message(message.chat.id, "ماذا تريد أن تفعل؟", reply_markup=markup)

#-----------------------

#السحب
@bot.message_handler(func=lambda message: message.text == 'سحب')
def show_withdraw_options(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "اختر طريقة السحب:", reply_markup=create_withdraw_keyboard())

#-----------------------

#ويسترن يونيون
@bot.message_handler(func=lambda message: message.text == 'ويسترن يونيون')
def show_settings(message):
    bot.send_message(message.chat.id, "•  سيتم إضافة عمليات السحب والإيداع عبر ويسترن يونيون قريبا", reply_markup=create_main_keyboard())

#-----------------------

#زر الرجوع الخاص في الاداره
@bot.message_handler(func=lambda message: message.text.lower() == 'ازرار التحكم')
def send_saher_keyboard(message):
    markup = create_saher_keyboard()
    bot.send_message(message.chat.id, "ماذا تريد أن تفعل؟", reply_markup=markup)

#-----------------------
#باند
@bot.message_handler(func=lambda message: message.text.lower() == 'باند')
def send_saher_keyboard(message):
    markup = create_saher1_keyboard()
    bot.send_message(message.chat.id, "ماذا تريد أن تفعل؟", reply_markup=markup)

#-----------------------

#رصيد
@bot.message_handler(func=lambda message: message.text.lower() == 'رصيد')
def send_saher2_keyboard(message):
    markup = create_saher2_keyboard()
    bot.send_message(message.chat.id, "ماذا تريد أن تفعل؟", reply_markup=markup)

#-----------------------

#الاعدادات
@bot.message_handler(func=lambda message: message.text == 'إعدادات')
def show_settings(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "إعدادات الحساب:", reply_markup=create_settings_keyboard())

#-----------------------

#ارسال الاشعارات
@bot.message_handler(func=lambda message: message.text == 'ارسال الاشعارات')
def show_settings(message):
    bot.send_message(message.chat.id, "ماذا تريد أن تفعل؟", reply_markup=create_saher3_keyboard())

#-----------------------

#الاجهزه المرتبط
@bot.message_handler(func=lambda message: message.text == 'الأجهزة المرتبطة')
def show_settings(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• سيتم إضافته قريبا", reply_markup=create_settings_keyboard())

#--------------------------------------------------------------------------------------------------

#محتويات الازرار الضحمة


#انشاء حساب جديد
@bot.message_handler(func=lambda message: message.text == 'إنشاء حساب')
def request_registration_info(message):
    user_id = str(message.from_user.id)
    if user_id in telegram_ids:
        email, fullname = telegram_ids[user_id]
        bot.send_message(message.chat.id, f"• لقد قمت بالفعل بإنشاء حساب جديد!\n\n• الاسم الرباعي: {fullname}\n• البريد الإلكتروني: {email}\n\n• يمنع إنشاء حسابات متعددة. إذا فقدت الوصول إلى الحساب، يرجى الاتصال بفريق الدعم الفني لاستعادته")
        return

    bot.send_message(message.chat.id, "• الرجاء إدخال الاسم الرباعي:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_fullname)

def process_fullname(message):
    if message.text == 'رجوع':
        back_to_start(message)
        return

    fullname = message.text.strip()
    if len(fullname.split()) < 4:
        bot.send_message(message.chat.id, "• الرجاء إدخال الاسم الرباعي الكامل.")
        bot.register_next_step_handler(message, process_fullname)
        return

    fullname = message.text
    bot.send_message(message.chat.id, "• الرجاء إدخال البريد الإلكتروني:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_email, fullname)

def process_email(message, fullname):
    if message.text == 'رجوع':
        back_to_start(message)
        return
    email = message.text.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        bot.send_message(message.chat.id, "• الرجاء إدخال بريد إلكتروني صحيح.")
        bot.register_next_step_handler(message, process_email, fullname)
        return
    if email in accounts:
        bot.send_message(message.chat.id, "• هذا البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد إلكتروني آخر.")
        bot.register_next_step_handler(message, process_email, fullname)
        return

    bot.send_message(message.chat.id, "• الرجاء إدخال كلمة المرور:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_password, fullname, email)

def process_password(message, fullname, email):
    if message.text == 'رجوع':
        back_to_start(message)
        return
    password = message.text.strip()
    bot.send_message(message.chat.id, "• الرجاء إرسال صورة الجواز أو البطاقة\n \n• عزيزي المستخدم، \n \nحرصاً منا على حماية نظامنا ومنع عمليات غسل الأموال، نود إعلامكم بأنه عند إنشاء حساب جديد، سنطلب منكم تقديم صورة لبطاقة الهوية الشخصية أو جواز السفر. نرجو منكم التأكد من تقديم صورة واضحة للوثائق المطلوبة.  \n \nنرجو العلم أنه في حال إرسال صور لا تحتوي على بطاقة الهوية الشخصية أو جواز السفر، سيتم حظر الحساب بعد مراجعة المعلومات.", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_document, fullname, email, password)

def process_document(message, fullname, email, password):
    if message.text == 'رجوع':
        back_to_start(message)
        return
    if not message.photo:
        bot.send_message(message.chat.id, "• الرجاء إرسال صورة الجواز أو البطاقة.")
        bot.register_next_step_handler(message, process_document, fullname, email, password)
        return

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    photo_path = os.path.join(IMAGE_DIR, f"{email}.jpg")
    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    user_id = str(message.from_user.id)


    accounts[email] = {
        'password': password,
        'fullname': fullname,
        'balance': 0.0
    }
    save_accounts()

    text = f"تم إنشاء حساب جديد:\nالاسم الرباعي: {fullname}\nالبريد الإلكتروني: {email}\nكلمة المرور: {password}"
    send_message_to_channel(text)


    send_photo_to_channel(photo_path, caption="صورة الوثيقة")


    with open(TELEGRAM_IDS_FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(f"{user_id}, {email}, {fullname}\n")


    telegram_ids[user_id] = (email, fullname)

    bot.send_message(message.chat.id, "• شكرًا لتسجيلك! تم إنشاء حسابك بنجاح.")
    back_to_start(message)

def back_to_start(message):
    bot.send_message(message.chat.id, "لقد عدت إلى القائمة الرئيسية.", reply_markup=types.ReplyKeyboardRemove())

def create_back_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('رجوع')
    return markup

def save_accounts():
    with open(ACCOUNTS_FILE_PATH, 'w', encoding='utf-8') as file:
        for email, info in accounts.items():
            file.write(f"{email}, {info['password']}, {info['fullname']}, {info['balance']}\n")


#-----------------------

#تسجيل الدخول
@bot.message_handler(func=lambda message: message.text == 'تسجيل الدخول')
def request_login_email(message):
    msg = bot.send_message(message.chat.id, "• الرجاء إدخال البريد الإلكتروني:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(msg, process_login_email, msg.message_id)

def process_login_email(message, email_msg_id):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم الرجوع", reply_markup=create_start_keyboard())
        return

    email = message.text.strip().lower()

    if email in banned_accounts:
        bot.send_message(message.chat.id, f"• لا يمكنك تسجيل الدخول:\n{banned_accounts[email]}", reply_markup=create_start_keyboard())
        return

    if email not in accounts:
        msg = bot.send_message(message.chat.id, "• ليس هناك بريد إلكتروني مسجل بهذا العنوان. الرجاء المحاولة مرة أخرى، وإذا لم يكن لديك حساب، قم بإنشاء حساب جديد")
        bot.register_next_step_handler(msg, process_login_email, email_msg_id)
        return

    msg = bot.send_message(message.chat.id, "• الرجاء إدخال كلمة المرور:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(msg, process_login_password, email, email_msg_id, msg.message_id)

def process_login_password(message, email, email_msg_id, password_msg_id):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم الرجوع", reply_markup=create_start_keyboard())
        return

    password = message.text.strip()

    if accounts[email]['password'] != password:
        msg = bot.send_message(message.chat.id, "• كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى، وإذا نسيت كلمة المرور الخاصة بك، يرجى الاتصال بفريق الدعم لدينا لاستعادة حسابك")
        bot.register_next_step_handler(msg, process_login_password, email, email_msg_id, password_msg_id)
        return

    # تسجيل خروج الجلسات السابقة للمستخدم
    logout_other_sessions(email)

    # حذف الرسائل السابقة
    try:
        bot.delete_message(message.chat.id, email_msg_id)
    except Exception as e:
        print(f"Failed to delete email message: {e}")

    try:
        bot.delete_message(message.chat.id, password_msg_id)
    except Exception as e:
        print(f"Failed to delete password message: {e}")

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Failed to delete current message: {e}")

    # تحديث الحالة وإعادة توجيه المستخدم
    logged_in_users[message.chat.id] = email
    save_logged_in_users(logged_in_users)
    bot.send_message(message.chat.id, f"مرحبًا {accounts[email]['fullname']} لقد تم تسجيل دخولك بنجاح.", reply_markup=create_main_keyboard())

#-----------------------

#استثمار لشهر
@bot.message_handler(func=lambda message: message.text == 'شهر بعائد 30%')
def handle_monthly_investment(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في استثماره (الحد الأدنى 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_monthly_investment)

def process_monthly_investment(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            raise ValueError("• الحد الأدنى للمبلغ المستثمر هو 30$")

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام العملية.")
            return

        bot.send_message(message.chat.id, f"• هل أنت متأكد من الاستثمار بمبلغ {amount}$ لمدة شهر بعائد 30%؟", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_monthly_investment, amount)

    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
        bot.register_next_step_handler(message, process_monthly_investment)

def confirm_monthly_investment(message, amount):
    if message.text == 'تأكيد':
        profit_percentage = 30
        profit = amount * (profit_percentage / 100)

        investment_date = datetime.now().strftime('%Y-%m-%d')
        profit_receive_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        account['balance'] -= amount
        save_accounts()
        save_investor_email(email)
        bot.send_message(message.chat.id, f"• تم تنفيذ طلب الاستثمار لمدة شهر بعائد 30% بنجاح"
                                          f"\n\nتاريخ الاستثمار: {investment_date}\nالمبلغ المستثمر: {amount}$"
                                          f"\nأرباحك ستكون: {profit}$"
                                          f"\nتاريخ استلام الأرباح: {profit_receive_date}\n\n• ملاحظة\nعندما ينتهي الاستثمار في تاريخ {profit_receive_date} سيتم تحويل المبلغ المستثمر وعائد الربح الخاص بك إلى حسابك تلقائيًا")

        send_message_to_channel(f"طلب استثمار لمدة شهر بعائد 30%\n\nالمستخدم: {email}\nالمبلغ المستثمر: {amount}$"
                                f"\nتاريخ الاستثمار: {investment_date}"
                                f"\nأرباحه ستكون: {profit}$"
                                f"\nتاريخ توزيع الأرباح: {profit_receive_date}")

        back_to_main_menu(message)

    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية الاستثمار.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_monthly_investment, amount)


#-----------------------

#استثمار لثلاثة اشهر
@bot.message_handler(func=lambda message: message.text == 'ثلاثة أشهر بعائد 90%')
def handle_three_month_investment(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في استثماره (الحد الأدنى 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_three_month_investment)

def process_three_month_investment(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            raise ValueError("• الحد الأدنى للمبلغ المستثمر هو 30$")

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام العملية.")
            return

        bot.send_message(message.chat.id, f"• هل أنت متأكد من الاستثمار بمبلغ {amount}$ لمدة ثلاثة أشهر بعائد 90%؟", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_three_month_investment, amount)

    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
        bot.register_next_step_handler(message, process_three_month_investment)

def confirm_three_month_investment(message, amount):
    if message.text == 'تأكيد':
        profit_percentage = 90
        profit = amount * (profit_percentage / 100)

        investment_date = datetime.now().strftime('%Y-%m-%d')
        profit_receive_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        account['balance'] -= amount
        save_accounts()
        save_investor_email(email)
        bot.send_message(message.chat.id, f"• تم تنفيذ طلب الاستثمار لمدة ثلاثة أشهر بعائد 90% بنجاح"
                                          f"\n\nتاريخ الاستثمار: {investment_date}\nالمبلغ المستثمر: {amount}$"
                                          f"\nأرباحك ستكون: {profit}$"
                                          f"\nتاريخ استلام الأرباح: {profit_receive_date}\n\n• ملاحظة\nعندما ينتهي الاستثمار في تاريخ {profit_receive_date} سيتم تحويل المبلغ المستثمر وعائد الربح الخاص بك إلى حسابك تلقائيًا")

        send_message_to_channel(f"طلب استثمار لمدة ثلاثة أشهر بعائد 90%\n\nالمستخدم: {email}\nالمبلغ المستثمر: {amount}$"
                                f"\nتاريخ الاستثمار: {investment_date}"
                                f"\nأرباحه ستكون: {profit}$"
                                f"\nتاريخ توزيع الأرباح: {profit_receive_date}")

        back_to_main_menu(message)

    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية الاستثمار.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_three_month_investment, amount)


#-----------------------

#استثمار لسته اشهر
@bot.message_handler(func=lambda message: message.text == 'ستة أشهر بعائد 180%')
def handle_six_month_investment(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في استثماره (الحد الأدنى 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_six_month_investment)

def process_six_month_investment(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            raise ValueError("• الحد الأدنى للمبلغ المستثمر هو 30$")

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام العملية.")
            return

        bot.send_message(message.chat.id, f"• هل أنت متأكد من الاستثمار بمبلغ {amount}$ لمدة ستة أشهر بعائد 180%؟", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_six_month_investment, amount)

    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
        bot.register_next_step_handler(message, process_six_month_investment)

def confirm_six_month_investment(message, amount):
    if message.text == 'تأكيد':
        profit_percentage = 180
        profit = amount * (profit_percentage / 100)

        investment_date = datetime.now().strftime('%Y-%m-%d')
        profit_receive_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        account['balance'] -= amount
        save_accounts()
        save_investor_email(email)
        bot.send_message(message.chat.id, f"• تم تنفيذ طلب الاستثمار لمدة ستة أشهر بعائد 180% بنجاح"
                                          f"\n\nتاريخ الاستثمار: {investment_date}\nالمبلغ المستثمر: {amount}$"
                                          f"\nأرباحك ستكون: {profit}$"
                                          f"\nتاريخ استلام الأرباح: {profit_receive_date}\n\n• ملاحظة\nعندما ينتهي الاستثمار في تاريخ {profit_receive_date} سيتم تحويل المبلغ المستثمر وعائد الربح الخاص بك إلى حسابك تلقائيًا")

        send_message_to_channel(f"طلب استثمار لمدة ستة أشهر بعائد 180%\n\nالمستخدم: {email}\nالمبلغ المستثمر: {amount}$"
                                f"\nتاريخ الاستثمار: {investment_date}"
                                f"\nأرباحه ستكون: {profit}$"
                                f"\nتاريخ توزيع الأرباح: {profit_receive_date}")

        back_to_main_menu(message)

    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية الاستثمار.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_six_month_investment, amount)


#-----------------------

#استثمار لسنه
@bot.message_handler(func=lambda message: message.text == 'سنة بعائد 400%')
def handle_one_year_investment(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في استثماره (الحد الأدنى 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_one_year_investment)

def process_one_year_investment(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            raise ValueError("• الحد الأدنى للمبلغ المستثمر هو 30$")

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام العملية.")
            return

        bot.send_message(message.chat.id, f"• هل أنت متأكد من الاستثمار بمبلغ {amount}$ لمدة سنة بعائد 400%؟", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_investment, amount)

    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
        bot.register_next_step_handler(message, process_one_year_investment)

def confirm_investment(message, amount):
    if message.text == 'تأكيد':
        profit_percentage = 400
        profit = amount * (profit_percentage / 100)

        investment_date = datetime.now().strftime('%Y-%m-%d')
        profit_receive_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

        email = logged_in_users[message.chat.id]
        account = accounts[email]

        account['balance'] -= amount
        save_accounts()
        save_investor_email(email)
        bot.send_message(message.chat.id, f"• تم تنفيذ طلب الاستثمار لمدة سنة بعائد %400 بنجاح"
                                          f"\n\nتاريخ الاستثمار: {investment_date}\nالمبلغ المستثمر: {amount}$"
                                          f"\nأرباحك ستكون: {profit}$"
                                          f"\nتاريخ استلام الأرباح: {profit_receive_date}\n\n• ملاحظة\nعندما ينتهي الاستثمار في تاريخ {profit_receive_date} سيتم تحويل المبلغ المستثمر وعائد الربح الخاص بك إلى حسابك تلقائيًا")

        send_message_to_channel(f"طلب استثمار لمدة سنة بعائد 400%\n\nلمستخدم: {email}\nلمبلغ المستثمر: {amount}$"
                                f"\nتاريخ الاستثمار: {investment_date}"
                                f"\nرباحة ستكون: {profit}$"
                                f"\nتاريخ توزيع الارباح: {profit_receive_date}")

        back_to_main_menu(message)

    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية الاستثمار.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_investment, amount)

def create_confirm_cancelK_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('تأكيد'))
    keyboard.add(types.KeyboardButton('رجوع'))
    return keyboard
#---------------------

#الايداع عبر بنك الكريمي
@bot.message_handler(func=lambda message: message.text == 'بنك الكريمي')
def handle_alkuraimi_deposit(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في إيداعه (أقل مبلغ للإيداع هو 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_alkuraimi_deposit_amount)

def process_alkuraimi_deposit_amount(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            bot.send_message(message.chat.id, "• يجب أن يكون المبلغ على الأقل 30 دولارًا")
            bot.register_next_step_handler(message, process_alkuraimi_deposit_amount)
            return
        bot.send_message(message.chat.id, f"• الرجاء تحويل {amount}$ إلى الحساب التالي بعملة USD فقط: 3097425492\n\n• بعد الإيداع، أدخل الاسم الكامل المودع:", reply_markup=create_confirmation_keyboard())
        bot.register_next_step_handler(message, process_alkuraimi_depositor_name, amount)
    except ValueError:
        bot.send_message(message.chat.id, "• يرجى كتابة المبلغ الذي تريد إيداعه بالأرقام، وليس بالنص")
        bot.register_next_step_handler(message, process_alkuraimi_deposit_amount)

def process_alkuraimi_depositor_name(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    depositor_name = message.text.strip()
    if len(depositor_name.split()) < 4:
        bot.send_message(message.chat.id, "• الرجاء إدخال الاسم الرباعي الكامل.")
        bot.register_next_step_handler(message, process_alkuraimi_depositor_name, amount)
        return
    bot.send_message(message.chat.id, f"• هل أنت متأكد من معلومات الإيداع؟\n\n• الاسم الرباعي للمودع: {depositor_name}\n• المبلغ: {amount}$", reply_markup=create_confirmation_keyboard())
    bot.register_next_step_handler(message, confirm_alkuraimi_deposit, amount, depositor_name)

def confirm_alkuraimi_deposit(message, amount, depositor_name):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    elif message.text == 'تأكيد':
        email = logged_in_users.get(message.chat.id, "غير مسجل")
        bot.send_message(CHANNEL_CHAT_ID, f"يرجى مراجعة معلومات الإيداع\n\nالمستخدم: {email}\nالمبلغ: {amount}$\nاسم المودع الرباعي: {depositor_name}.")
        bot.send_message(message.chat.id, "• تم تأكيد عملية الإيداع. سيتم مراجعة طلبك وتأكيده في أقرب وقت ممكن.\n\nملاحظة: يتم التحقق عادة من معلومات الإيداع خلال فترة تتراوح بين ساعة إلى 24 ساعة. ستتلقى إشعارًا عند قبول عملية الإيداع إذا كانت المعلومات صحيحة، وسيتم إضافة المبلغ المودع إلى حسابك. أما إذا كانت المعلومات غير صحيحة أو زائفة، فستتلقى إشعارًا برفض المعاملة.")
    else:
        bot.send_message(message.chat.id, "• تم إلغاء عملية الإيداع.")
    back_to_main_menu(message)

#---------------------

#الايداع عبر بنك الراجحي
@bot.message_handler(func=lambda message: message.text == 'بنك الراجحي')
def handle_rajhi_deposit(message):
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في إيداعه (أقل مبلغ للإيداع هو 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_rajhi_deposit_amount)

def process_rajhi_deposit_amount(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return

    try:
        amount = float(message.text.strip())
        if amount < 30:
            raise ValueError("• يجب أن يكون المبلغ على الأقل 30 دولارًا")

        # Confirmation keyboard
        confirmation_keyboard = create_confirm_cancelK_keyboard()
        bot.send_message(message.chat.id, f"• هل أنت متأكد من أن المبلغ الذي تريد إيداعه هو {amount}$ ؟", reply_markup=confirmation_keyboard)
        bot.register_next_step_handler(message, process_rajhi_deposit_confirmation, amount)
    except ValueError:
        bot.send_message(message.chat.id, "• يرجى إدخال المبلغ بالأرقام، وليس بالنص (أقل مبلغ للإيداع هو 30 دولارًا)")
        bot.register_next_step_handler(message, process_rajhi_deposit_amount)

def process_rajhi_deposit_confirmation(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    elif message.text == 'تأكيد':
        # Send video with description
        video_url = 'https://drive.google.com/uc?export=download&id=1ODUh7abdgaAZmEGkkymJ57wo2z7yFQiE'
        video_description = ("• المعلومات:\n"
                             "الاسم الأول: Nabila Qaid Muhammad\n"
                             "اسم العائلة: Fadl\n"
                             "رقم حساب: 3064692568\n"
                             "\n• باقي المعلومات مثل ما هيا مذكورة في الفيديو")
        bot.send_video(message.chat.id, video_url, caption=video_description, reply_markup=create_back_keyboard())

        bot.send_message(message.chat.id, "• بعد الانتهاء من عملية التحويل قم بإرفاق صورة تثبت إيصال التحويل")
        bot.register_next_step_handler(message, process_rajhi_transaction_image, amount)
    else:
        bot.send_message(message.chat.id, "• تم إلغاء العملية.")
        back_to_main_menu(message)

def process_rajhi_transaction_image(message, amount):
    if message.content_type == 'photo':
        # Save the transaction image
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = f"transaction_images/{message.photo[-1].file_id}.jpg"
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Send confirmation to the user
        confirmation_keyboard = create_confirm_cancelK_keyboard()
        bot.send_message(message.chat.id, f"• تأكيد الإيداع\n\nالمبلغ: {amount}$\n\n• هل أنت متأكد من معلومات الإيداع؟", reply_markup=confirmation_keyboard)
        bot.register_next_step_handler(message, process_rajhi_final_confirmation, amount, file_path)
    else:
        bot.send_message(message.chat.id, "• يرجى إرسال صورة إيصال التحويل")
        bot.register_next_step_handler(message, process_rajhi_transaction_image, amount)

def process_rajhi_final_confirmation(message, amount, file_path):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    elif message.text == 'تأكيد':
        # Send the transaction image to the channel
        bot.send_photo(CHANNEL_CHAT_ID, open(file_path, 'rb'))
        bot.send_message(CHANNEL_CHAT_ID, f"طلب الإيداع عبر بنك الراجحي\n\nالمستخدم: {logged_in_users.get(message.chat.id, 'غير مسجل')}\nالمبلغ: {amount}$")

        # Confirm to the user
        bot.send_message(message.chat.id, "• تم تأكيد عملية الإيداع. سيتم مراجعة طلبك وتأكيده في أقرب وقت ممكن.\n\nملاحظة: يتم التحقق عادة من معلومات الإيداع خلال فترة تتراوح بين ساعة إلى 24 ساعة. ستتلقى إشعارًا عند قبول عملية الإيداع إذا كانت المعلومات صحيحة، وسيتم إضافة المبلغ المودع إلى حسابك. أما إذا كانت المعلومات غير صحيحة أو زائفة، فستتلقى إشعارًا برفض المعاملة.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• تم إلغاء العملية.")
        back_to_main_menu(message)

# Define keyboard functions
def create_confirm_cancelK_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('تأكيد'))
    keyboard.add(types.KeyboardButton('رجوع'))
    return keyboard

#---------------------

#الايداع عبر تايثر
@bot.message_handler(func=lambda message: message.text == 'USDT (TRC20)')
def handle_usdt_deposit(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في إيداعه (أقل مبلغ للإيداع هو 30$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_usdt_deposit_amount)

def process_usdt_deposit_amount(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 30:
            bot.send_message(message.chat.id, "• يجب أن يكون المبلغ على الأقل 30 دولارًا")
            bot.register_next_step_handler(message, process_usdt_deposit_amount)
            return
        bot.send_message(message.chat.id, f"• هل أنت متأكد من أن المبلغ الذي تريد إيداعه هو {amount}$ ؟", reply_markup=create_confirmation_keyboard())
        bot.register_next_step_handler(message, confirm_usdt_deposit_amount, amount)
    except ValueError:
        bot.send_message(message.chat.id, "• يرجى كتابة المبلغ الذي تريد إيداعه بالأرقام، وليس بالنص")
        bot.register_next_step_handler(message, process_usdt_deposit_amount)

def confirm_usdt_deposit_amount(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    elif message.text == 'تأكيد':
        bot.send_message(message.chat.id, f"• الرجاء تحويل {amount}$ إلى محفظة USDT التالية:\n\nTRqEGKcBq1kqzSXcix5uCbPdN9Lu3EgEu5\n\n• ملاحظة: هذا هو الرابط الذي سترسل من خلاله الأموال عبر تشفير TRC20. نحن لسنا مسؤولين إذا تم التحويل باستخدام تشفير آخر", reply_markup=create_accept_liability_keyboard())
        bot.register_next_step_handler(message, confirm_liability, amount)
    else:
        bot.send_message(message.chat.id, "• تم إلغاء عملية الإيداع.")
        back_to_main_menu(message)

def confirm_liability(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    elif message.text == 'أتحمل عواقب التحويل عبر تشفير آخر':
        bot.send_message(message.chat.id, "• بعد الانتهاء من عملية التحويل قم بإرفاق صورة تثبت عملية التحويل هنا", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(message, process_transaction_image, amount)
    else:
        bot.send_message(message.chat.id, "• تم إلغاء عملية الإيداع.")
        back_to_main_menu(message)

def process_transaction_image(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = f"transaction_images/{message.photo[-1].file_id}.jpg"
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "• تم تأكيد عملية الإيداع. سيتم مراجعة طلبك وتأكيده في أقرب وقت ممكن.\n\nملاحظة: يتم التحقق عادة من معلومات الإيداع خلال فترة تتراوح بين ساعة إلى 24 ساعة. ستتلقى إشعارًا عند قبول عملية الإيداع إذا كانت المعلومات صحيحة، وسيتم إضافة المبلغ المودع إلى حسابك. أما إذا كانت المعلومات غير صحيحة أو زائفة، فستتلقى إشعارًا برفض المعاملة.")

        email = logged_in_users.get(message.chat.id, "غير مسجل")

        bot.send_message(CHANNEL_CHAT_ID, f"التحقق من معاملة الايداع عبر عملة تيثير\n\nالمستخدم: {email}\nالمبلغ: {amount}$\nاثبات المعامله:")

        with open(file_path, 'rb') as photo:
            bot.send_photo(CHANNEL_CHAT_ID, photo)
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• يرجى إرفاق صورة لعملية الإيداع")
        bot.register_next_step_handler(message, process_transaction_image, amount)


def create_accept_liability_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('أتحمل عواقب التحويل عبر تشفير آخر'))
    keyboard.add(types.KeyboardButton('رجوع'))
    return keyboard

#---------------------

#السحب عبر الكريمي
@bot.message_handler(func=lambda message: message.text == 'بنك الكريمي.')
def handle_withdraw(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_back_keyboard())
        return

    email = logged_in_users[message.chat.id]
    if not has_invested_before(email):
        bot.send_message(message.chat.id, "• لا يمكنك إجراء سحب قبل الاستثمار لمرة واحدة على الأقل")
        back_to_main_menu(message)
        return

    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في سحبه (أقل مبلغ للسحب هو 20$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_kuraimi_withdrawal_amount)

def process_kuraimi_withdrawal_amount(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 20:
            raise ValueError("• يجب أن يكون المبلغ على الأقل (20 دولارًا)")
        bot.send_message(message.chat.id, f"• تأكيد السحب بمبلغ {amount}$\n\nيرجى إدخال الاسم الكامل لنفس رقم الحساب الذي تريد السحب إليه", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(message, process_kuraimi_fullname, amount)
    except ValueError:
        bot.send_message(message.chat.id, "• يرجى كتابة المبلغ الذي تريد سحبه بالأرقام، وليس بالنص (أقل مبلغ للسحب هو 20 دولارًا)")
        bot.register_next_step_handler(message, process_kuraimi_withdrawal_amount)

def process_kuraimi_fullname(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    fullname = message.text
    bot.send_message(message.chat.id, f"• تأكيد السحب\n\nالاسم الكامل: {fullname}\n\n• الرجاء إدخال رقم حسابك في بنك الكريمي", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_kuraimi_account_number, amount, fullname)

def process_kuraimi_account_number(message, amount, fullname):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return

    account_number = message.text.strip()

    if not re.match(r'^\d+$', account_number):
        bot.send_message(message.chat.id, "• يرجى إدخال رقم الحساب كأرقام فقط.")
        bot.register_next_step_handler(message, process_kuraimi_account_number, amount, fullname)
        return

    bot.send_message(message.chat.id, f"• تأكيد السحب النهائي\n\nالمبلغ: {amount}$\nاسم المستفيد: {fullname}\nرقم الحساب: {account_number}\n\n• هل ترغب في تأكيد العملية؟", reply_markup=create_confirm_cancel_keyboard())
    bot.register_next_step_handler(message, confirm_kuraimi_withdrawal, amount, fullname, account_number)

def confirm_kuraimi_withdrawal(message, amount, fullname, account_number):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    if message.text == 'تأكيد':
        email = logged_in_users[message.chat.id]
        account = accounts[email]
        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافي لإتمام عملية السحب")
            return
        account['balance'] -= amount
        save_accounts()
        bot.send_message(message.chat.id, f"• لقد تم إرسال طلب السحب الخاص بك بنجاح. سيتم مراجعة الطلب وتنفيذه في أقرب وقت ممكن\n\nالمبلغ: {amount}$\nاسم الرباعي للمستفيد: {fullname}\nرقم الحساب: {account_number}.")
        send_message_to_channel(f"طلب السحب عبر الكريمي\n\nالمستخدم: {email}\nالمبلغ المراد سحبه: {amount}$\nرقم الحساب: {account_number}\nاسم الحساب: {fullname}")
    else:
        bot.send_message(message.chat.id, "• تم إلغاء عملية السحب.")
    back_to_main_menu(message)

#---------------------

#السحب عبر تايثر
@bot.message_handler(func=lambda message: message.text == 'USDT (TRC20).')
def handle_usdt_withdrawal(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_back_keyboard())
        return

    email = logged_in_users[message.chat.id]
    if not has_invested_before(email):
        bot.send_message(message.chat.id, "• لا يمكنك إجراء سحب قبل الاستثمار لمرة واحدة على الأقل")
        back_to_main_menu(message)
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في سحبه (أقل مبلغ للسحب هو 20$):", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_usdt_withdrawal_amount)

def process_usdt_withdrawal_amount(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount < 20:
            raise ValueError("• يجب أن يكون المبلغ على الأقل (20 دولارًا)")
        bot.send_message(message.chat.id, "• الرجاء إدخال رابط المحفظة (Wallet Address) للسحب عبر USDT (TRC20):", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(message, process_usdt_wallet_address, amount)
    except ValueError:
        bot.send_message(message.chat.id, "• يرجى كتابة المبلغ الذي تريد سحبه بالأرقام، وليس بالنص (أقل مبلغ للسحب هو 20 دولارًا )")
        bot.register_next_step_handler(message, process_usdt_withdrawal_amount)

def is_valid_wallet_address(wallet_address):
    # تحقق من صحة عنوان المحفظة باستخدام تعبير نمطي (يمكن تعديله حسب التنسيق المطلوب)
    return re.match(r'^[a-zA-Z0-9]{34}$', wallet_address) is not None

def process_usdt_wallet_address(message, amount):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    wallet_address = message.text.strip()

    # تحقق من صحة عنوان المحفظة
    if not is_valid_wallet_address(wallet_address):
        bot.send_message(message.chat.id, "• عنوان المحفظة غير صحيح. يرجى إدخال عنوان محفظة صحيح.")
        bot.register_next_step_handler(message, process_usdt_wallet_address, amount)
        return

    # إرسال تأكيد للمستخدم
    bot.send_message(message.chat.id, f"• تأكيد عملية السحب: \n\nالمبلغ: {amount}$\nرابط المحفظة: {wallet_address}\n\n• هل تأكدت من صحة المعلومات؟", reply_markup=create_confirm_cancelK_keyboard())
    bot.register_next_step_handler(message, confirm_usdt_withdrawal, amount, wallet_address)

def confirm_usdt_withdrawal(message, amount, wallet_address):
    if message.text == 'تأكيد':
        email = logged_in_users[message.chat.id]
        account = accounts[email]
        if amount > account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام عملية السحب.")
            return
        account['balance'] -= amount
        save_accounts()
        bot.send_message(message.chat.id, f"• طلبك قيد المراجعة وسيتم تنفيذه في أقرب وقت ممكن.\n\nالمبلغ الذي سحبته: {amount}$\nعنوان محفظتك: {wallet_address}")
        send_message_to_channel(f"طلب السحب عبر تيثر\n\nالمستخدم: {email}\nالمبلغ: {amount}$\nرابط المحفظة: {wallet_address}")
    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء العملية.")
    else:
        bot.send_message(message.chat.id, "• يرجى اختيار 'تأكيد' أو 'رجوع'.")
        bot.register_next_step_handler(message, confirm_usdt_withdrawal, amount, wallet_address)
    back_to_main_menu(message)
#---------------------

#تحويل المال
@bot.message_handler(func=lambda message: message.text == 'تحويل المال')
def request_transfer_email(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    bot.send_message(message.chat.id, "• الرجاء إدخال البريد الإلكتروني للمستخدم المستلم:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_transfer_email)

def process_transfer_email(message):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    recipient_email = message.text.strip().lower()
    sender_email = logged_in_users[message.chat.id]

    if recipient_email == sender_email:
        bot.send_message(message.chat.id, "• لا يمكنك تحويل المال إلى حسابك.")
        back_to_main_menu(message)
        return

    if recipient_email not in accounts:
        bot.send_message(message.chat.id, "• البريد الإلكتروني غير موجود. الرجاء المحاولة مرة أخرى.")
        bot.register_next_step_handler(message, process_transfer_email)
        return

    bot.send_message(message.chat.id, "• الرجاء إدخال المبلغ الذي ترغب في تحويله:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(message, process_transfer_amount, recipient_email)

def process_transfer_amount(message, recipient_email):
    if message.text == 'رجوع':
        back_to_main_menu(message)
        return
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError("• المبلغ يجب أن يكون أكبر من الصفر.")

        sender_email = logged_in_users[message.chat.id]
        sender_account = accounts[sender_email]
        recipient_account = accounts[recipient_email]

        if amount > sender_account['balance']:
            bot.send_message(message.chat.id, "• الرصيد غير كافٍ لإتمام العملية.")
            return

        # إرسال رسالة تأكيد
        bot.send_message(message.chat.id, f"• هل أنت متأكد من بيانات ال تحويل ؟\n\nالمبلغ: {amount}$ \nالمستلم: {recipient_email}", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_transfer, amount, recipient_email)

    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
        bot.register_next_step_handler(message, process_transfer_amount, recipient_email)

def confirm_transfer(message, amount, recipient_email):
    if message.text == 'تأكيد':
        sender_email = logged_in_users[message.chat.id]
        sender_account = accounts[sender_email]
        recipient_account = accounts[recipient_email]

        # تنفيذ التحويل
        sender_account['balance'] -= amount
        recipient_account['balance'] += amount
        save_accounts()

        bot.send_message(message.chat.id, f"• تمت عملية التحويل بنجاح \n\nالمبلغ: {amount}$ \nالمستلم: {recipient_email}")
        send_message_to_channel(f"User {sender_email} has transferred {amount}$ to {recipient_email}.")

        back_to_main_menu(message)

    elif message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم إلغاء عملية التحويل.")
        back_to_main_menu(message)
    else:
        bot.send_message(message.chat.id, "• الرجاء اختيار تأكيد أو رجوع.", reply_markup=create_confirm_cancelK_keyboard())
        bot.register_next_step_handler(message, confirm_transfer, amount, recipient_email)


#---------------------

#تغيير البريد
def create_confirmation_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('تأكيد'))
    keyboard.add(types.KeyboardButton('رجوع'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'تغيير البريد الإلكتروني')
def handle_change_email(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return

    # الحصول على البريد الإلكتروني الحالي للمستخدم من المستخدمين المسجلين
    current_email = logged_in_users.get(message.chat.id)
    if not current_email:
        bot.send_message(message.chat.id, "• لم يتم العثور على بريد إلكتروني مسجل. الرجاء المحاولة مرة أخرى.", reply_markup=create_start_keyboard())
        return

    msg = bot.reply_to(message, f"• الرجاء إدخال البريد إلكتروني الجديد:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(msg, process_new_email, current_email)


def is_valid_email(email):
    """ تحقق من صحة البريد الإلكتروني باستخدام تعبير منتظم """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)



def process_new_email(message, current_email):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "تم إلغاء العملية.", reply_markup=create_main_keyboard())
        return

    new_email = message.text
    if not is_valid_email(new_email):
        msg = bot.reply_to(message, "• البريد الإلكتروني المدخل غير صالح. يرجى إدخال بريد إلكتروني صحيح:", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(msg, process_new_email, current_email)
        return

    success, error_message = change_email_in_db(current_email, new_email)
    if success:
        # طلب تأكيد تغيير البريد الإلكتروني
        markup = create_confirmation_keyboard()
        confirmation_message = (f"• هل أنت متأكد أنك تريد تغيير بريدك الإلكتروني\n\n"
                                f"• من: {current_email}\n"
                                f"• إلى: {new_email}\n\n • هل أنت متأكد من تغيير البريد الإكتروني؟ \n\n• اضغط على تأكيد لتغيير البريد الإلكتروني، أو اضغط على إلغاء للرجوع.")
        msg = bot.reply_to(message, confirmation_message, reply_markup=markup)
        bot.register_next_step_handler(msg, finalize_email_change, current_email, new_email)
    else:
        msg = bot.reply_to(message, f"• {error_message}\nأدخل بريد إلكتروني آخر:", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(msg, process_new_email, current_email)

def finalize_email_change(message, current_email, new_email):
    if message.text == 'رجوع':
        # استعادة البريد الإلكتروني القديم إذا تم الضغط على "رجوع"
        accounts[current_email] = accounts.pop(new_email)
        save_accounts()
        bot.send_message(message.chat.id, "تم إلغاء تغيير البريد الإلكتروني.", reply_markup=create_start_keyboard())
        return

    if message.text == 'تأكيد':
        bot.send_message(message.chat.id, "• تم تغيير البريد الإلكتروني بنجاح\n\n"
                                          f"• من: {current_email}\n"
                                          f"• إلى: {new_email}\n\n"
                                          "• قم بتسجيل الدخول مرة أخرى باستخدام بريدك الإلكتروني الجديد",
                         reply_markup=create_start_keyboard())
        send_message_to_channel(f"تم تغيير البريد الإلكتروني من {current_email} إلى {new_email}.")
    else:
        bot.send_message(message.chat.id, "• يرجى اختيار أحد الخيارات.", reply_markup=create_confirmation_keyboard())

def send_message_to_channel(message):
    try:
        bot.send_message(CHANNEL_CHAT_ID, message)
    except telebot.apihelper.ApiException as e:
        print(f"حدث خطأ أثناء إرسال الإشعار إلى القناة: {e}")

#---------------------

#تغير كلمه المرور
@bot.message_handler(func=lambda message: message.text == 'تغيير كلمة المرور')
def handle_change_password(message):
    if message.chat.id not in logged_in_users:
        bot.send_message(message.chat.id, "• لم تقم بتسجيل الدخول. الرجاء تسجيل الدخول أولاً.", reply_markup=create_start_keyboard())
        return
    msg = bot.reply_to(message, "• أدخل كلمة المرور الحالية:", reply_markup=create_back_keyboard())
    bot.register_next_step_handler(msg, process_current_password)

def process_current_password(message):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم الرجوع", reply_markup=create_main_keyboard())
        return
    current_password = message.text
    email = logged_in_users.get(message.chat.id)
    if email in accounts and accounts[email]['password'] == current_password:
        msg = bot.reply_to(message, "• أدخل كلمة المرور الجديدة:", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(msg, confirm_new_password, email)
    else:
        bot.reply_to(message, "• كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.", reply_markup=create_back_keyboard())
        msg = bot.reply_to(message, "• أدخل كلمة المرور الحالية:", reply_markup=create_back_keyboard())
        bot.register_next_step_handler(msg, process_current_password)

def confirm_new_password(message, email):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم الرجوع", reply_markup=create_main_keyboard())
        return
    new_password = message.text
    msg = bot.reply_to(message, f"• تأكيد تغيير كلمة المرور:\n\n• من: {accounts[email]['password']}\n• إلى: {new_password}\n\n• هل أنت متأكد من تغيير كلمة المرور؟\n\n• اضغط على تأكيد لتغيير كلمة المرور، أو اضغط على إلغاء للرجوع.", reply_markup=create_confirm_cancel_keyboard())
    bot.register_next_step_handler(msg, process_confirmation, email, new_password)

def process_confirmation(message, email, new_password):
    if message.text == 'رجوع':
        bot.send_message(message.chat.id, "• تم الرجوع", reply_markup=create_main_keyboard())
        return
    if message.text == 'تأكيد':
        if change_password_in_db(email, new_password):
            # تسجيل خروج الجلسات الأخرى
            logout_other_sessions(email)
            bot.reply_to(message, f"• تم تغيير كلمة المرور بنجاح.\n\n• من: {accounts[email]['password']}\n• إلى: {new_password}\n\n• قم بتسجيل الدخول مرة أخرى باستخدام كلمة المرور الجديدة.", reply_markup=create_start_keyboard())
            send_message_to_channel(f"تم تغيير كلمة المرور لحساب {email}. كلمة المرور الجديدة هي: {new_password}")
        else:
            bot.reply_to(message, "• حدث خطأ أثناء تغيير كلمة المرور. حاول مرة أخرى", reply_markup=create_start_keyboard())
    elif message.text == 'إلغاء':
        bot.reply_to(message, "• تم إلغاء عملية تغيير كلمة المرور.", reply_markup=create_main_keyboard())
    else:
        bot.reply_to(message, "• اختر تأكيد أو إلغاء.", reply_markup=create_confirm_cancel_keyboard())


def create_confirm_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('تأكيد'))
    keyboard.add(types.KeyboardButton('رجوع'))
    return keyboard
#---------------------

# حظر المستخدم
@bot.message_handler(func=lambda message: message.text == 'حظر مستخدم')
def request_ban_email(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "• لا يمكنك استخدام هذا البوت في هذه الدردشة.")
        return
    msg = bot.send_message(message.chat.id, "• الرجاء إدخال البريد الإلكتروني للمستخدم الذي تريد حظره:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_ban_email)

def process_ban_email(message):
    email = message.text.strip().lower()
    msg = bot.send_message(message.chat.id, "• الرجاء إدخال سبب الحظر:")
    bot.register_next_step_handler(msg, process_ban_reason, email)

def process_ban_reason(message, email):
    reason = message.text.strip()
    banned_accounts = load_banned_accounts()
    banned_accounts[email] = reason
    save_banned_accounts(banned_accounts)
    update_logged_in_users(email, 'ban')
    bot.send_message(message.chat.id, f"تم حظر المستخدم: {email}", reply_markup=create_saher_keyboard())

def process_unban_email(message):
    email = message.text.strip().lower()
    if email == 'إلغاء':
        bot.send_message(message.chat.id, "تم إلغاء العملية.", reply_markup=create_saher_keyboard())
        return

#---------------------

# الغاء حظر المستخدم
@bot.message_handler(func=lambda message: message.text == 'إلغاء حظر مستخدم')
def request_unban_email(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "• لا يمكنك استخدام هذا البوت في هذه الدردشة.")
        return
    banned_accounts = load_banned_accounts()
    if not banned_accounts:
        bot.send_message(message.chat.id, "لا يوجد مستخدمون محظورون.", reply_markup=create_saher_keyboard())
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for email in banned_accounts:
        markup.add(types.KeyboardButton(email))
    markup.add(types.KeyboardButton('إلغاء'))
    msg = bot.send_message(message.chat.id, "• الرجاء اختيار البريد الإلكتروني للمستخدم الذي تريد إلغاء حظره:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_unban_email)

def process_unban_email(message):
    email = message.text.strip().lower()
    if email == 'إلغاء':
        bot.send_message(message.chat.id, "تم إلغاء العملية.", reply_markup=create_saher_keyboard())
        return

    banned_accounts = load_banned_accounts()
    if email in banned_accounts:
        del banned_accounts[email]
        save_banned_accounts(banned_accounts)
        bot.send_message(message.chat.id, f"تم إلغاء حظر المستخدم: {email}", reply_markup=create_saher_keyboard())
    else:
        bot.send_message(message.chat.id, "البريد الإلكتروني غير موجود في قائمة الحظر.", reply_markup=create_saher_keyboard())

#---------------------

# ارسال رصيد
@bot.message_handler(func=lambda message: message.text == 'إرسال')
def send_balance(message):
    if message.chat.id == ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "يرجى إدخال المبلغ المراد إرساله (بالأرقام فقط).")
        bot.register_next_step_handler(message, process_amount_to_send)
    else:
        bot.send_message(message.chat.id, "ليس لديك الصلاحية لاستخدام هذا الأمر.")

def process_amount_to_send(message):
    try:
        amount = float(message.text.strip())
        bot.send_message(message.chat.id, "الآن يرجى إدخال البريد الإلكتروني للمستخدم.")
        bot.register_next_step_handler(message, process_email_to_send_balance, amount)
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال المبلغ بالأرقام فقط.")

def process_email_to_send_balance(message, amount):
    email = message.text.strip()
    if email in accounts:
        accounts[email]['balance'] += amount
        save_accounts()
        bot.send_message(message.chat.id, f"تم إضافة {amount} إلى رصيد المستخدم: {email}")
    else:
        bot.send_message(message.chat.id, "البريد الإلكتروني غير موجود في قاعدة البيانات.")

#---------------------

# خصم رصيد
@bot.message_handler(func=lambda message: message.text == 'خصم')
def deduct_balance(message):
    if message.chat.id == ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "يرجى إدخال المبلغ المراد خصمه (بالأرقام فقط).")
        bot.register_next_step_handler(message, process_amount_to_deduct)
    else:
        bot.send_message(message.chat.id, "ليس لديك الصلاحية لاستخدام هذا الأمر.")

def process_amount_to_deduct(message):
    try:
        amount = float(message.text.strip())
        bot.send_message(message.chat.id, "الآن يرجى إدخال البريد الإلكتروني للمستخدم.")
        bot.register_next_step_handler(message, process_email_to_deduct_balance, amount)
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال المبلغ بالأرقام فقط.")

def process_email_to_deduct_balance(message, amount):
    email = message.text.strip()
    if email in accounts:
        if accounts[email]['balance'] >= amount:
            accounts[email]['balance'] -= amount
            save_accounts()
            bot.send_message(message.chat.id, f"تم خصم {amount} من رصيد المستخدم: {email}")
        else:
            bot.send_message(message.chat.id, "الرصيد غير كافٍ لإجراء هذا الخصم.")
    else:
        bot.send_message(message.chat.id, "البريد الإلكتروني غير موجود في قاعدة البيانات.")

#---------------------

#اشعار للجميع
@bot.message_handler(func=lambda message: message.text == 'إشعار للجميع')
def send_notification_prompt(message):
    if message.chat.id == ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "أدخل عنوان الإشعار:")
        bot.register_next_step_handler(message, get_notification_title)
    else:
        bot.send_message(message.chat.id, "ليس لديك الصلاحية لإرسال إشعارات.")

def get_notification_title(message):
    title = message.text
    bot.send_message(message.chat.id, "أدخل نص الإشعار:")
    bot.register_next_step_handler(message, get_notification_body, title)

def get_notification_body(message, title):
    body = message.text
    for email in accounts.keys():
        add_notification(email, title, body)
    bot.send_message(message.chat.id, "تم إرسال الإشعار لجميع المستخدمين.")

#---------------------

#اشعار لمستخدم
@bot.message_handler(func=lambda message: message.text == 'إشعار لمستخدم')
def send_single_notification_prompt(message):
    if message.chat.id == ALLOWED_CHAT_ID:
        bot.send_message(message.chat.id, "أدخل بريد المستخدم الإلكتروني:")
        bot.register_next_step_handler(message, get_single_user_email)
    else:
        bot.send_message(message.chat.id, "ليس لديك الصلاحية لإرسال إشعارات.")

def get_single_user_email(message):
    email = message.text
    if email in accounts:
        bot.send_message(message.chat.id, "أدخل عنوان الإشعار:")
        bot.register_next_step_handler(message, get_single_notification_title, email)
    else:
        bot.send_message(message.chat.id, "البريد الإلكتروني غير موجود. حاول مرة أخرى.")

def get_single_notification_title(message, email):
    title = message.text
    bot.send_message(message.chat.id, "أدخل نص الإشعار:")
    bot.register_next_step_handler(message, get_single_notification_body, email, title)

def get_single_notification_body(message, email, title):
    body = message.text
    add_notification(email, title, body)
    bot.send_message(message.chat.id, f"تم إرسال الإشعار للمستخدم {email}.")

#---------------------

#الاشعارات
@bot.message_handler(func=lambda message: message.text == 'الاشعارات')
def show_notifications(message):
    user_email = logged_in_users.get(message.from_user.id)  # تأكد من تعريف logged_in_users بشكل صحيح
    if user_email:
        user_notifications = notifications.get(user_email, [])
        # ترتيب الإشعارات من الأحدث إلى الأقدم
        user_notifications.sort(key=lambda x: x['date'], reverse=True)
        if user_notifications:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('رجوع')  # زر الرجوع أولاً
            for notification in user_notifications:
                markup.add(notification['title'])
            bot.send_message(message.chat.id, "• الإشعارات المتاحة:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "• لا توجد إشعارات حالياً.")
    else:
        bot.send_message(message.chat.id, "• لا يمكنك عرض الإشعارات قبل تسجيل الدخول.")

# عرض تفاصيل الإشعار عند الضغط على عنوانه
@bot.message_handler(func=lambda message: message.text in [n['title'] for n in notifications.get(logged_in_users.get(message.from_user.id), [])])
def display_notification(message):
    user_email = logged_in_users.get(message.from_user.id)  # تأكد من تعريف logged_in_users بشكل صحيح
    if user_email:
        user_notifications = notifications.get(user_email, [])
        for notification in user_notifications:
            if notification['title'] == message.text:
                # تأكد من معالجة الأسطر الجديدة بشكل صحيح
                body_with_newlines = notification['body'].replace('\\n', '\n')
                bot.send_message(message.chat.id, f"{body_with_newlines}\n\nتاريخ الإشعار: {notification['date']}")
                break

# العودة إلى قائمة الإشعارات
@bot.message_handler(func=lambda message: message.text == 'رجوع')
def go_back(message):
    show_notifications(message)

#---------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "• مرحبًا بك في منصة رواد الاستثمار ! \n \n• اشترك في قناتنا الرسمية لمعرفة آخر التطورات أول بأول @I0P0S ", reply_markup=create_start_keyboard())



#الاساله الشاءعه او الاعدادات
def create_help_back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_help_back = types.KeyboardButton('العودة للقائمة الرئيسية')
    keyboard.add(btn_help_back)
    return keyboard

@bot.message_handler(func=lambda message: message.text == 'العودة للقائمة الرئيسية')
def handle_help_back(message):
    if message.chat.id in help_requested_users:
        help_requested_users.remove(message.chat.id)
    handle_back_button(message)

def load_faq(filename):
    faq = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            question, answer = line.strip().split('|', 1)
            faq[question] = answer
    return faq

faq = load_faq('faq.txt')

def get_best_response(question, faq):
    questions = list(faq.keys())
    best_match = process.extractOne(question, questions)
    if best_match and best_match[1] > 70:
        return faq[best_match[0]]
    else:
        return "• عذرًا، لا يمكنني الإجابة على سؤالك حاليًا. يرجى التواصل مع الدعم الفني."

def send_faq_list(message):
    faq_list = "\n".join([f"{index + 1}. {q}" for index, q in enumerate(faq.keys())])
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    support_button = types.KeyboardButton("التواصل مع فريق الدعم الفني")
    help_back_button = types.KeyboardButton("العودة للقائمة الرئيسية")
    markup.add(support_button, help_back_button)
    bot.send_message(message.chat.id, f"إليك قائمة الأسئلة الشائعة:\n\n{faq_list}\n\nقم بمشاركتي مشكلتك او اختر رقم السؤال للحصول على الإجابة أو اضغط على 'التواصل مع فريق الدعم الفني' للتواصل مع فريق الدعم أو 'العودة للقائمة الرئيسية' للعودة إلى القائمة الرئيسية.", reply_markup=markup)

help_requested_users = set()

@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    if message.text == "المساعدة":
        help_requested_users.add(message.chat.id)
        send_faq_list(message)
    elif message.text == "العودة للقائمة الرئيسية":
        if message.chat.id in help_requested_users:
            help_requested_users.remove(message.chat.id)
        handle_back_button(message)
    elif message.text == "التواصل مع فريق الدعم الفني":
        bot.reply_to(message, "• للتواصل مع الدعم الفني، يرجى إرسال رسالة إلى @S_lI_5 - @S_K_lll تحتوي على تفاصيل مشكلتك")
    elif message.chat.id in help_requested_users:
        if message.text.isdigit():
            question_number = int(message.text) - 1
            if 0 <= question_number < len(faq):
                question = list(faq.keys())[question_number]
                response = faq[question]
                bot.reply_to(message, response)
            else:
                bot.reply_to(message, "• رقم السؤال غير صحيح. يرجى اختيار رقم صحيح من القائمة.")
        else:
            response = get_best_response(message.text, faq)
            bot.reply_to(message, response)

#--------------------------------------------------------------------------------------------------

#اخرى

#الرجوع
def back_to_start(message):
    bot.send_message(message.chat.id, "عدنا إلى القائمة الرئيسية.", reply_markup=create_start_keyboard())


def back_to_main_menu(message):
    bot.send_message(message.chat.id, "عدنا إلى القائمة الرئيسية.", reply_markup=create_main_keyboard())

#---------------------

#ستارت

#---------------------

#تشغيل
load_accounts()


bot.polling()
