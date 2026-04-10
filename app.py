python
import os
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- ያንተን የቻፓ ኮድ እዚህ አስገባ ---
CHAPA_SECRET_KEY = 'CHASECK_TEST-RXB1XrByfzYA98xJLFBDcisRQQaviTxN' 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fayda Card Maker</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #f4f7f6; padding: 40px; }
        .card { background: white; padding: 30px; border-radius: 15px; max-width: 400px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn { background: #1e40af; color: white; padding: 12px; border: none; width: 100%; border-radius: 5px; cursor: pointer; font-size: 18px; margin-top: 20px; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .price { color: #059669; font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>የፋይዳ መታወቂያ መቀየሪያ</h2>
        <p>ፒዲኤፍ ፋይልዎን ወደ ካርድ ይቀይሩ</p>
        <p class="price">ዋጋ፦ 40 ብር</p>
        <form action="/pay" method="POST">
            <input type="email" name="email" placeholder="ኢሜይልዎን ያስገቡ" required>
            <button type="submit" class="btn">ክፍያ ፈጽም</button>
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
        return f"ስህተት፦ {data.get('message')}"
    except Exception as e:
        return f"ችግር ተፈጥሯል፦ {str(e)}"


if __name__ == "__main__":
    # Render የሚሰጠውን PORT ይጠቀማል፣ ካልተገኘ ግን 10000 ይጠቀማል
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
