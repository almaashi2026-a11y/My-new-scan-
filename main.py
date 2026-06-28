import os
import asyncio
import yfinance as yf
from telegram import Bot

# الحصول على الإعدادات من Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# دالة الفحص (محدثة لتتوافق مع نظام Async)
async def scan_stocks():
    symbols = ["AAPL", "GNTA", "EZGO"] 
    while True:
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                data = stock.history(period="1d")
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    message = f"🚀 تحديث سهم {symbol}: {last_price:.2f}$"
                    # إضافة await هنا تحل مشكلة التنبيه
                    await bot.send_message(chat_id=CHAT_ID, text=message)
                await asyncio.sleep(20) 
            except Exception as e:
                print(f"خطأ في فحص {symbol}: {e}")
                await asyncio.sleep(60)

# تشغيل البوت
if __name__ == "__main__":
    asyncio.run(scan_stocks())
