import os
import time
import asyncio
import yfinance as yf
from telegram import Bot

# إعدادات البوت
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

symbols = ["AAPL", "GNTA", "EZGO"] 

# تحويل الدالة إلى async لتتوافق مع مكتبة التليجرام الجديدة
async def scan_stocks():
    while True:
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                data = stock.history(period="1d")
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    message = f"🚀 تحديث سهم {symbol}: {last_price:.2f}$"
                    # استخدام await للاتصال بتليجرام
                    await bot.send_message(chat_id=CHAT_ID, text=message)
                
                await asyncio.sleep(20) # انتظار غير متزامن
                
            except Exception as e:
                print(f"خطأ في فحص {symbol}: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    print("البوت بدأ العمل الآن بنظام Async...")
    # تشغيل الحلقة الأساسية
    asyncio.run(scan_stocks())
    
