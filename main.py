import os
import time
import yfinance as yf
from telegram import Bot

# الحصول على الإعدادات من Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# قائمة الأسهم
symbols = ["AAPL", "GNTA", "EZGO"] 

def scan_stocks():
    for symbol in symbols:
        try:
            # استخدام مكتبة yfinance بشكل أكثر استقراراً
            stock = yf.Ticker(symbol)
            # جلب آخر سعر فقط بطريقة أخف
            data = stock.history(period="1d")
            
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                message = f"🚀 تحديث سهم {symbol}: {last_price:.2f}$"
                bot.send_message(chat_id=CHAT_ID, text=message)
            
            # زيادة وقت الانتظار لتجنب الحظر تماماً
            time.sleep(20) 
            
        except Exception as e:
            print(f"خطأ في فحص {symbol}: {e}")
            # إذا حدث خطأ، انتظر دقيقة كاملة قبل المحاولة التالية
            time.sleep(60)

if __name__ == "__main__":
    print("البوت بدأ العمل الآن...")
    while True:
        scan_stocks()
