import os, requests
from flask import Flask, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@fahim_trading_pro")

def get_btc_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return 112000 + random.randint(-500,500)

def generate_signal():
    price = get_btc_price()
    direction = random.choice(["LONG 📈", "SHORT 📉"])
    leverage = random.choice(["10x","20x","25x","50x"])
    entry = price
    if "LONG" in direction:
        tp1 = entry * 1.008
        tp2 = entry * 1.015
        sl = entry * 0.992
    else:
        tp1 = entry * 0.992
        tp2 = entry * 0.985
        sl = entry * 1.008
    
    return {
        "pair": "BTC/USDT",
        "price": f"{entry:,.2f}",
        "dir": direction,
        "lev": leverage,
        "entry": f"{entry:,.2f}",
        "tp1": f"{tp1:,.2f}",
        "tp2": f"{tp2:,.2f}",
        "sl": f"{sl:,.2f}",
        "time": datetime.now().strftime("%d %b, %I:%M %p")
    }

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fahim Trading Pro</title>
<style>
body{background:#0a0e13;color:white;font-family:Arial;text-align:center;padding:20px}
.card{background:#151a21;border-radius:15px;padding:20px;max-width:400px;margin:auto;border:1px solid #2a3441}
.price{font-size:32px;color:#00ff88;font-weight:bold}
.dir{font-size:28px;margin:15px 0;padding:10px;border-radius:10px;background:#1f2937}
.info{text-align:left;background:#0f141b;padding:15px;border-radius:10px;margin:15px 0;line-height:1.8}
.btn{background:#00ff88;color:black;padding:15px 30px;border:none;border-radius:10px;font-size:18px;font-weight:bold;width:100%;margin-top:10px}
.btn2{background:#0088ff;color:white;padding:12px;border:none;border-radius:10px;width:100%;margin-top:10px}
.live{color:#00ff88;border:1px solid #00ff88;padding:5px 15px;border-radius:20px;font-size:12px}
</style>
</head>
<body>
<span class="live">● BOT LIVE</span>
<h2>FAHIM TRADING PRO</h2>
<div class="card">
<div class="price">$ {{ s.price }}</div>
<div>{{ s.pair }} • {{ s.time }}</div>
<div class="dir">{{ s.dir }} {{ s.lev }}</div>
<div class="info">
<b>Entry:</b> ${{ s.entry }}<br>
<b>TP1:</b> ${{ s.tp1 }} 🎯<br>
<b>TP2:</b> ${{ s.tp2 }} 🎯<br>
<b>SL:</b> ${{ s.sl }} 🛑<br>
</div>
<form action="/send" method="post">
<button class="btn">📤 Send to Telegram</button>
</form>
<a href="/"><button class="btn2">🔄 New Signal</button></a>
</div>
<p style="color:#5
