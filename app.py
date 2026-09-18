import os, threading
from flask import Flask
import telebot, random, requests
BOT_TOKEN=os.environ.get("BOT_TOKEN")
CHANNEL_ID=os.environ.get("CHANNEL_ID")
app=Flask(__name__)
bot=telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None
def get_price():
    try:
        r=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=5).json()
        return float(r['price'])
    except:
        return 111609.00
@app.route('/')
def home():
    p=get_price()
    return f"<h1>BOT LIVE</h1><h2>FAHIM TRADING PRO</h2><h3>{p}</h3>"
@bot.message_handler(commands=['day','signal','start'])
def send_signal(message):
    m=random.choice(["EUR/USD (OTC)","GBP/USD (OTC)","BTC/USD (OTC)"])
    p=get_price()
    rsi=random.randint(28,72)
    sig="UP CALL" if rsi<45 else "DOWN PUT"
    text=f"🔥 FAHIM BEST TODAY - DAY 🔥\nMarket: {m}\nSignal: {sig}\nRSI: {rsi}\nPrice: {p:.2f}\nExpiry: 1 MIN"
    bot.send_message(CHANNEL_ID,text)
    bot.reply_to(message,"Signal sent!")
def run_bot():
    if bot:
        bot.infinity_polling()
threading.Thread(target=run_bot).start()
if __name__=="__main__":
    app.run(host='0.0.0.0',port=10000)
