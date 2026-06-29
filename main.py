import os
from telegram import Bot
import asyncio

async def test_bot():
    bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
    chat_id = os.environ.get("CHAT_ID")
    print(f"محاولة إرسال رسالة إلى {chat_id}")
    try:
        await bot.send_message(chat_id=chat_id, text="البوت يعمل بنجاح! 🚀")
        print("تم إرسال الرسالة بنجاح.")
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
        
