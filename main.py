import os
import time
import yfinance as yf
from telegram import Bot

# الحصول على الإعدادات من Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# قائمة الأسهم التي تتابعها
symbols = ["AAPL", "GNTA", "EZGO"] 

def scan_stocks():
    for symbol in symbols:
        try:
            # جلب البيانات
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d", interval="1m")
            
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                message = f"سهم {symbol} بسعر {last_price:.2f}"
                bot.send_message(chat_id=CHAT_ID, text=message)
            
            # إضافة تأخير لتجنب الحظر من ياهو (مهم جداً!)
            time.sleep(10) 
            
        except Exception as e:
            print(f"خطأ في فحص {symbol}: {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("البوت بدأ العمل الآن...")
    while True:
        scan_stocks()
        # انتظار دقيقة قبل بدء جولة فحص جديدة
        time.sleep(60)
