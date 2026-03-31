import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
app = Flask(__name__)

# إعداد مفتاح الـ API - تأكد من وضعه في ملف .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, mode TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not openai.api_key:
        return jsonify({"reply": "⚠️ خطأ: لم يتم ضبط API Key في السيرفر."}), 500
        
    data = request.json
    user_msg = data.get("message")
    mode = data.get("mode", "normal")

    system_prompt = "أنت خبير برمجة (Python, Lua, Discord Bots). قدم أكواداً كاملة واحترافية."
    
    if mode == "thinking":
        system_prompt += "\n[وضع التفكير العميق]: حلل المنطق البرمجي بدقة قصوى."
        temp = 0.2
    else:
        temp = 0.7

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # أو gpt-4 إذا كان حسابك يدعمه
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=temp
        )
        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "❌ الـ API لا يستجيب. تأكد من الرصيد أو المفتاح."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
