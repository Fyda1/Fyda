python
import os
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- RXB1XrByfzYA98xJLFBDcisRQQaviTxN ---
CHAPA_SECRET_KEY = 'RXB1XrByfzYA98xJLFBDcisRQQaviTxN' 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fayda ID Converter</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; text-align: center; background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
        .card { background: white; color: #333; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); max-width: 400px; width: 90%; }
        h1 { color: #1e40af; margin-bottom: 10px; }
        .price { font-size: 35px; color: #059669; font-weight: bold; margin: 20px 0; }
        .btn { background: #1e40af; color: white; padding: 15px; border: none; border-radius: 10px; font-size: 18px; width: 100%; cursor: pointer; text-decoration: none; display: block; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Fayda ID</h1>
        <p>ፒዲኤፍዎን ወደ ካርድ ለመቀየር 40 ብር ይክፈሉ</p>
        <div class="price">40 ETB</div>
        <form action="/pay" method="POST">
            <input type="email" name="email" placeholder="ኢሜይልዎን ያስገቡ" required>
            <button type="submit" class="btn">ክፍያ ይፈጽሙ</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/pay', methods=['POST'])
def pay():
    email = request.form.get('email')
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    payload = {
        "amount": "40",
        "currency": "ETB",
        "email": email,
        "tx_ref": f"fayda-{os.urandom(4).hex()}",
        "callback_url": "https://chapa.co",
        "return_url": "https://chapa.co"
    }
    try:
        response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        data = response.json()
        if data.get('status') == 'success':
            return redirect(data['data']['checkout_url'])
        return f"ስህተት ተፈጥሯል: {data.get('message')}"
    except:
        return "ግንኙነት ተቋርጧል። እባክዎ ድጋሚ ይሞክሩ።"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
