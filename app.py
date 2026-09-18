import os, threading
from flask import Flask
import telebot, random, requests
BOT_TOKEN=os.environ.get("BOT_TOKEN")
CHANNEL_ID=os.environ.get("CHANNEL_ID")
app=Flask(__name__)
@app.route('/')
def home():
    try:
        r=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=3).json()
        p=float(r['price'])
    except:
        p=111609.00
    return f"<h1>BOT LIVE</h1><h3>{p}</h3>"
if BOT_TOKEN:
    bot=telebot.TeleBot(BOT_TOKEN)
    @bot.message_handler(commands=['day','signal','start'])
    def send_signal(message):
        try:
            r=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=3).json()
            p=float(r['price'])
        except:
            p=111609.00
        m=random.choice(["EUR/USD (OTC)","GBP/USD (OTC)","BTC/USD (OTC)"])
        rsi=random.randint(28,72)
        sig="UP CALL" if rsi<45 else "DOWN PUT"
        text=f"🔥 FAHIM BEST TODAY - DAY 🔥\nMarket: {m}\nSignal: {sig}\nRSI: {rsi}\nPrice: {p:.2f}"
        bot.send_message(CHANNEL_ID,text)
        bot.reply_to(message,"Sent!")
    def run_bot():
        bot.infinity_polling()
    threading.Thread(target=run_bot,daemon=True).start()
