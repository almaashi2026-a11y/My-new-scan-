import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import random
import requests
from telegram import Bot

# جلب الإعدادات من Render (تأكد من إضافتها في Environment Variables)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

def fetch_penny_stocks():
    # جلب قائمة الأسهم تحت 10$ تلقائياً
    url = "https://finviz.com/export.ashx?v=111&f=sh_price_u10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        data = response.text.split('\n')
        symbols = [line.split(',')[1].replace('"', '') for line in data[1:] if len(line) > 2]
        return symbols
    except:
        return ["AAPL", "AMD", "NVDA"]

def scan_market():
    symbols = fetch_penny_stocks()
    random.shuffle(symbols) # الخلط العشوائي
    
    for symbol in symbols:
        try:
            df = yf.download(symbol, period="2d", interval="5m", progress=False)
            if df.empty or len(df) < 15: continue
            
            last_price = df['Close'].iloc[-1]
            
            # المؤشرات
            df['EMA9'] = ta.ema(df['Close'], length=9)
            df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
            
            # التقاطع الإيجابي
            if (df['EMA9'].iloc[-2] < df['VWAP'].iloc[-2]) and (df['EMA9'].iloc[-1] > df['VWAP'].iloc[-1]):
                msg = f"🎯 **فرصة مكتشفة:** {symbol}\n💰 السعر: {last_price:.2f}$\n📈 التقاطع: EMA9 تجاوز VWAP"
                bot.send_message(chat_id=CHAT_ID, text=msg)
                time.sleep(2)
        except:
            continue

while True:
    scan_market()
    time.sleep(600) # انتظار 10 دقائق بعد كل جولة
