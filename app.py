import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()
app = Flask(__name__)

# ملاحظة: ضع مفتاحك هنا لمرة واحدة أو في ملف .env
openai.api_key = os.getenv("OPENAI_API_KEY", "ضع_مفتاحك_هنا")

def get_db():
    conn = sqlite3.connect('ai_platform.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS sessions 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS messages 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, role TEXT, content TEXT, 
                        FOREIGN KEY(session_id) REFERENCES sessions(id))''')
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sessions', methods=['GET'])
def get_sessions():
    with get_db() as conn:
        sessions = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    return jsonify([dict(s) for s in sessions])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    session_id = data.get("session_id")
    mode = data.get("mode", "normal")

    with get_db() as conn:
        # إذا كانت محادثة جديدة، أنشئ جلسة وسمّها
        if not session_id:
            title = user_msg[:30] + "..." if len(user_msg) > 30 else user_msg
            cur = conn.execute("INSERT INTO sessions (title) VALUES (?)", (title,))
            session_id = cur.lastrow_id
        
        conn.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, 'user', user_msg))
        conn.commit()

    # إعداد الـ Prompt المتخصص للبرمجة
    system_p = "أنت خبير برمجة (Python, Lua). قدم أكواداً كاملة واحترافية."
    temp = 0.2 if mode == "thinking" else 0.7

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_p}, {"role": "user", "content": user_msg}],
            temperature=temp
        )
        ai_reply = response.choices[0].message.content
        
        with get_db() as conn:
            conn.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, 'assistant', ai_reply))
            conn.commit()

        return jsonify({"reply": ai_reply, "session_id": session_id})
    except:
        return jsonify({"reply": "⚠️ خطأ: تأكد من صلاحية الـ API Key الخاص بك."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
