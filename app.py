import os, requests
from flask import Flask, jsonify
app = Flask(__name__)
BOT=os.environ.get("TELEGRAM_BOT_TOKEN","")
CHAT=os.environ.get("TELEGRAM_CHANNEL_ID","@fahim_trading_pro")
@app.route("/")
def home():
 return f"<h1>BOT LIVE</h1><button onclick=\"fetch('/send',{{method:'POST'}}).then(r=>r.json()).then(d=>alert(d.msg))\">Send</button>"
@app.route("/send",methods=["POST"])
def send():
 if not BOT:
  return jsonify(msg="Token add korle jabe! USDJPY BUY")
 r=requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage",json={"chat_id":CHAT,"text":"USD/JPY BUY RSI 29"},timeout=10)
 return jsonify(msg=f"Sent {r.status_code}")
app.run(host="0.0.0.0",port=10000)
