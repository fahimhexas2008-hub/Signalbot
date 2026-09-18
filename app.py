import os, requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN","").strip()
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID","").strip()

HTML = """
<html><body style='background:#000;color:#0f0;text-align:center;padding:20px;font-family:Arial'>
<h2>QUOTEX PRO v2.0 FIXED</h2>
<p>Token: OK | Channel: @fahim_trading_pro</p>
<h1>GBP/USD - SELL</h1>
<button onclick="send()" style="padding:15px 30px;background:#00aaff;color:white;border:none;border-radius:10px;font-size:18px">📤 Send to Telegram</button>
<p id="msg"></p>
<script>
function send(){
 fetch('/send_telegram',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pair:'GBP/USD (OTC)',signal:'SELL',rsi:77})})
 .then(r=>r.json()).then(d=>{alert(d.message); document.getElementById('msg').innerText=d.message})
}
</script>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/send_telegram", methods=["POST"])
def send_tg():
    if not BOT_TOKEN:
        return jsonify(message="Token Missing! Render Check করুন")
    data = request.json
    text = f"🔥 SIGNAL: {data['pair']} {data['signal']} RSI {data['rsi']}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    if r.status_code == 200:
        return jsonify(message="Signal Sent Successfully! ✅")
    else:
        return jsonify(message=f"Telegram Error: {r.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
