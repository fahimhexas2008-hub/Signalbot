import os, threading, time
from flask import Flask
import telebot, random, requests

BOT_TOKEN=os.environ.get("BOT_TOKEN")
CHANNEL_ID=os.environ.get("CHANNEL_ID")

app=Flask(__name__)

@app.route('/')
def home():
    return "<h1>BOT LIVE - Fahim</h1><h3>Running 24/7</h3>"

# বট চালু করার ফাংশন
def start_bot():
    if not BOT_TOKEN: 
        print("BOT_TOKEN নাই!")
        return
    bot = telebot.TeleBot(BOT_TOKEN)
    
    @bot.message_handler(commands=['day','signal','start'])
    def send_signal(message):
        m=random.choice(["EUR/USD (OTC)","GBP/USD (OTC)","BTC/USD (OTC)"])
        rsi=random.randint(28,72)
        sig="UP CALL 🟢" if rsi<45 else "DOWN PUT 🔴"
        text=f"🔥 FAHIM BEST TODAY 🔥\nMarket: {m}\nSignal: {sig}\nRSI: {rsi}\nTime: 1 MIN"
        try:
            bot.send_message(CHANNEL_ID,text)
            bot.reply_to(message,"✅ Channel e pathano hoise!")
        except Exception as e:
            bot.reply_to(message,f"Error: {e} - Bot ke channel er admin koro nai!")
    
    print("Bot Polling Start...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)

# থ্রেডে বট চালু - এইটাই আসল ফিক্স
threading.Thread(target=start_bot, daemon=True).start()
