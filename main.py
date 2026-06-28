import os
import yfinance as yf
import pandas as pd
import time
import random
import requests
from telegram import Bot

# جلب الإعدادات من إعدادات Render (Environment Variables)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

def fetch_penny_stocks():
    # جلب قائمة الأسهم تحت 10$ من Finviz
    url = "https://finviz.com/export.ashx?v=111&f=sh_price_u10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.text.split('\n')
        symbols = [line.split(',')[1].replace('"', '') for line in data[1:] if len(line) > 2]
        return symbols
    except:
        return ["AAPL", "AMD", "NVDA", "TSLA"]

def scan_market():
    symbols = fetch_penny_stocks()
    random.shuffle(symbols) # خلط الأسهم
    
    for symbol in symbols:
        try:
            # تحميل بيانات آخر يومين
            df = yf.download(symbol, period="2d", interval="5m", progress=False)
            if df.empty or len(df) < 15: continue
            
            last_price = df['Close'].iloc[-1]
            
            # حساب المؤشرات يدوياً بدون مكتبات معقدة
            # EMA 9
            df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
            
            # VWAP يدوياً
            df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['VWAP'] = (df['TP'] * df['Volume']).cumsum() / df['Volume'].cumsum()
            
            # شرط التقاطع
            if (df['EMA9'].iloc[-2] < df['VWAP'].iloc[-2]) and (df['EMA9'].iloc[-1] > df['VWAP'].iloc[-1]):
                msg = f"🚀 فرصة صيد: {symbol}\n💰 السعر: {last_price:.2f}$\n📈 تم التقاطع"
                bot.send_message(chat_id=CHAT_ID, text=msg)
                time.sleep(2) # انتظار لتجنب الحظر
        except:
            continue

# حلقة التشغيل الدائم
while True:
    try:
        scan_market()
    except Exception as e:
        print(f"خطأ في الحلقة: {e}")
    time.sleep(600) # فحص شامل كل 10 دقائق
