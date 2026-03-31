import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

# تحميل الإعدادات
load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# إعداد قاعدة البيانات لحفظ المحادثات
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
    data = request.json
    user_msg = data.get("message")
    mode = data.get("mode") # normal, thinking, quick

    # تخصيص ذكاء المبرمج (Python, Lua, Discord)
    system_prompt = (
        "أنت خبير برمجة محترف. لغاتك الأساسية هي Python و Lua. "
        "خبير في بناء بوتات Discord. أجب دائماً بأكواد كاملة ونظيفة."
    )

    if mode == "thinking":
        system_prompt += "\n[وضع التفكير العميق]: حلل المنطق البرمجي بدقة، لا تختصر الكود، وتجنب الأخطاء المنطقية."
        temp = 0.1
    elif mode == "quick":
        system_prompt += "\n[وضع سريع]: أجب باختصار مفيد ومباشر."
        temp = 0.8
    else:
        temp = 0.5

    try:
        # حفظ رسالة المستخدم في القاعدة
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO chat (role, content, mode) VALUES (?, ?, ?)", ('user', user_msg, mode))

        # طلب الرد من الذكاء الاصطناعي
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            temperature=temp
        )
        ai_reply = response.choices[0].message.content

        # حفظ رد الذكاء الاصطناعي
        c.execute("INSERT INTO chat (role, content, mode) VALUES (?, ?, ?)", ('assistant', ai_reply, mode))
        conn.commit()
        conn.close()

        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"❌ خطأ: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)
