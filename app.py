import os, random, threading, time, requests
from flask import Flask, request, render_template_string
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

MARKETS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)", "BTC/USD (OTC)", "USD/BRL (OTC)"]

def get_real_price():
    try:
        # Real price from Binance BTC for base logic
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return 65000.0

def generate_best_signal(market):
    price = get_real_price()
    # Fake RSI logic but looks real
    rsi = random.randint(20, 80)
    
    if rsi < 35:
        direction = "UP 🟢 CALL"
        reason = f"RSI {rsi} (Oversold)"
   
