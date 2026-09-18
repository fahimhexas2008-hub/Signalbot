import os,random,threading,requests
from flask import Flask,request,render_template_string
import telebot

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")
bot=telebot.TeleBot(BOT_TOKEN)
app=Flask(__name__)

MARKETS=["EUR/USD (OTC)","GBP/USD (OTC)","USD/JPY (OTC)","BTC/USD (OTC)"]

def get_price():
 try:
  r=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=5).json()
  return float(r['price'])
 except:
  return 65000.0

def make_signal(m):
 p=get_price()
 rsi=random.randint(28,72)
 sig="UP 🟢 CALL" if rsi<45 else "DOWN 🔴 PUT"
 return f"🔥 *FAHIM BEST TODAY* 🔥\n\n💰 Market: *{m}*\n📊 Signal: *{sig}*\n📈 RSI: {rsi}\n💵 Price: {p:.2f}\n\n⏰ Expiry: 1 MIN\n💸 MM: 1% Balance\n✅ Max 2 Martingale"

def send_sig(m):
 t=make_signal(m)
 bot.send_message(CHANNEL_ID,t,parse_mode="Markdown")
 return t

@app.route("/")
def home():
 return render_template_string('<center style="background:#000;color:#fff;padding:30px;"><h2 style="color:#0f6;">● LIVE TODAY</h2><select id="m" style="padding:12px;width:80%;">{%for x in mk%}<option>{{x}}</option>{%endfor%}</select><br><br><button onclick="location.href=\'/send?market=\'+document.getElementById(\'m\').value" style="padding:15px 30px;background:#0f6;font
