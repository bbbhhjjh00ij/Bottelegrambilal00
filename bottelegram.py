import subprocess
import sys
import logging
import asyncio
from fastapi import FastAPI
from telegram import Update, filters
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
import re

# تثبيت المكتبات المطلوبة إذا لم تكن موجودة
def install_packages():
    required_packages = [
        'fastapi', 
        'uvicorn', 
        'python-telegram-bot'
    ]
    
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# تثبيت المكتبات إذا كانت غير موجودة
install_packages()

# توكن البوت و ID المشرف
TOKEN = '7453518539:AAGaUdf10iCqauTXGJfGDxOHel_xzv3T4CI'
ADMIN_ID = 7971415230

# إعدادات السجل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# إعداد FastAPI
app = FastAPI()

# ترحيب المستخدم الجديد
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    welcome_msg = await update.message.reply_text(f"مرحباً {user.first_name} ({user.username})!\n\nID: {user.id}")
    
    # حذف الرسالة بعد ساعة (3600 ثانية)
    await asyncio.sleep(3600)
    await welcome_msg.delete()
    logger.info(f"تم حذف الرسالة التي تحتوي على ID بعد ساعة: {welcome_msg.text}")

# حذف الرسالة التي تحتوي على ID
async def message_handler(update: Update, context: CallbackContext) -> None:
    # فحص ما إذا كانت الرسالة تحتوي على ID (رقم من 9-12 خانة)
    if re.search(r'\d{9,12}', update.message.text):
        await update.message.delete()  # حذف الرسالة
        logger.info(f"تم حذف الرسالة لأنها تحتوي على ID: {update.message.text}")

# إعداد الوظائف
async def main():
    application = Application.builder().token(TOKEN).build()

    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))

    # التعامل مع الرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # تشغيل البوت
    await application.run_polling()

# تشغيل البوت في الخلفية عبر FastAPI
@app.on_event("startup")
async def start_bot():
    # تشغيل البوت في الخلفية
    asyncio.create_task(main())

# نقطة البداية للـ FastAPI
@app.get("/")
async def read_root():
    return {"message": "بوت تيليجرام يعمل باستخدام FastAPI"}
