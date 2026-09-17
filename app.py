from flask import Flask
import random
app = Flask(__name__)
@app.route('/')
def home():
    s=random.choice(["BUY","SELL"])
    p=random.choice(["EURUSD","GBPUSD","USDJPY"])
    c="lime" if s=="BUY" else "red"
    return f"<body style='background:black;color:white;text-align:center;padding-top:80px'><h1>QUOTEX BOT LIVE</h1><h2>{p}</h2><h1 style='color:{c};font-size:60px'>{s}</h1><button onclick='location.reload()'>Next</button></body>"
if __name__=='__main__':
    app.run()
