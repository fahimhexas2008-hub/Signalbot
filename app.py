import os, threading, time
from flask import Flask, render_template_string, request
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@fahim_trading_pro")
app = Flask(__name__)

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return 111514.00

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:white;font-family:sans-serif;text-align:center;padding:20px}
.card{background:#1a1a1a;border-radius:20px;padding:20px;max-width:400px;margin:auto;border:1px solid #333}
.price{color:#00ff88;font-size:36px;font-weight:bold}
.btn-green{background:#00ff88;color:black;padding:15px;border-radius:12px;width:100%;border:none;font-size:18px;font-weight:bold;margin-top:15px}
.btn-blue{background:#1e90ff;color:white;padding:12px;border-radius:12px;width:100%;border:none;margin-top:10px}
</style></head><body>
<div class="card">
<div class="price">$ {{price}}</div>
<div>{{time}}</div>
<div style="background:#2a2a3a;padding:12px;border-radius:12px;margin-top:15px">LONG 25x</div>
<p>TP1: ${{tp1}} | TP2: ${{tp2}} | SL: ${{sl}}</p>
<form action="/send" method="post"><input type="hidden" name="price" value="{{price}}">
<button class="btn-green">📤 Send to Telegram</button></form>
<button class="btn-blue" onclick="location.reload()">🔄 New Signal</button>
<p style="color:{{color}}">{{status}}</p>
</div></body></html>
"""

@app.route('/')
def home():
    p=get_price()
    return render_template_string(HTML, price=f"{p:,.2f}", time=time.strftime("%d %b %I:%M %p"), tp1=f"{p*1.008:,.2f}", tp2=f"{p*1.015:,.2f}", sl=f"{p*0.992:,.2f}", status="Ready", color="gray")

@app.route('/send', methods=['POST'])
def send():
    price=request.form.get('price','0')
    txt=f"🔥 FAHIM TRADING PRO 🔥\nBTC: ${price}\nLONG 25x\nTP +0.8% | SL -0.8%\n{time.strftime('%d %b %I:%M %p')}"
    try:
        telebot.TeleBot(BOT_TOKEN).send_message(CHANNEL_ID, txt)
        st="✅ Telegram e chole geche!"; col="#00ff88"
    except Exception as e:
        st=f"❌ Bot ke channel e Admin koro! {e}"; col="red"
    p=get_price()
    return render_template_string(HTML, price=f"{p:,.2f}", time=time.strftime("%d %b %I:%M %p"), tp1=f"{p*1.008:,.2f}", tp2=f"{p*1.015:,.2f}", sl=f"{p*0.992:,.2f}", status=st, color=col)

def run_bot():
    if not BOT_TOKEN: return
    b=telebot.TeleBot(BOT_TOKEN); b.remove_webhook(); time.sleep(2)
    while True:
        try: b.infinity_polling(timeout=60, long_polling_timeout=60)
        except: time.sleep(5)
threading.Thread(target=run_bot, daemon=True).start()
