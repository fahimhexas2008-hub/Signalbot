import os,random,threading,time,requests
from flask import Flask,request,render_template_string
import telebot
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")
bot=telebot.TeleBot(BOT_TOKEN)
app=Flask(__name__)
MARKETS=["EUR/USD (OTC)","GBP/USD (OTC)","USD/JPY (OTC)","AUD/USD (OTC)","BTC/USD (OTC)"]
def get_price():
 try:return float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=5).json()['price'])
 except:return 65000.0
def make_signal(m):
 p=get_price();rsi=random.randint(25,75);d="UP 🟢 CALL" if rsi<40 else "DOWN 🔴 PUT" if rsi>60 else random.choice(["UP 🟢 CALL","DOWN 🔴 PUT"])
 return f"🔥 *FAHIM BEST TODAY* 🔥\n💰 Market: *{m}*\n📊 Signal: *{d}*\n📈 RSI: {rsi} | Price: {p:.2f}\n📍 Sup: {p*0.9985:.2f}\n📍 Res: {p*1.0015:.2f}\n⏰ 1 MIN\n💸 Risk 1% | 2 Marti Max | 3 Win=STOP"
def send_sig(m):
 t=make_signal(m);bot.send_message(CHANNEL_ID,t,parse_mode="Markdown");return t
@app.route("/")
def home():return render_template_string('<body style="background:#000;color:#fff;text-align:center;padding:30px;"><h2 style="color:#0f6;">● BEST BOT LIVE TODAY</h2><select id="m" style="padding:15px;width:90%;background:#222;color:#fff;">{%for x in mk%}<option>{{x}}</option>{%endfor%}</select><br><br><button onclick="location.href=\'/send?market=\'+document.getElementById(\'m\').value" style="padding:18px;background:#0f6;color:#000;font-size:20px;border-radius:12px;font-weight:bold;">📤 SEND BEST SIGNAL</button></body>',mk=MARKETS)
@app.route("/send")
def s_route():
 m=request.args.get("market","EUR/USD (OTC)");send_sig(m);return f"<center><h1>✅ SENT {m}</h1><a href='/'>Back</a></center>"
thread
