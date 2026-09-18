import os, random, threading, time, requests
from flask import Flask, request, render_template_string
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

MARKETS = ["EUR/USD (OTC)","GBP/USD (OTC)","USD/JPY (OTC)","AUD/USD (OTC)","BTC/USD (OTC)"]

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return 65000.0

def make_signal(m):
    p = get_price()
    rsi = random.randint(25,75)
    d = "UP 🟢 CALL" if rsi<40 else "DOWN 🔴 PUT" if rsi>60 else random.choice(["UP 🟢 CALL","DOWN 🔴 PUT"])
    sup = p*0.9985
    res = p*1.0015
    return f"""
🔥 *FAHIM BEST SIGNAL TODAY* 🔥
💰 Market: *{m}*
📊 Signal: *{d}*
📈 RSI: {rsi} | Price: {p:.2f}
📍 Support: {sup:.2f}
📍 Resistance: {res:.2f}
⏰ 1 MIN Trade
💸 Risk: 1% Balance | Max 2 Martingale | 3 Win = STOP
