from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数読み込み
load_dotenv()

print("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", os.getenv("OPENAI_API_KEY"))  # ←これ！

# Flask 初期化
app = Flask(__name__)
CORS(app)

# OpenAI クライアント初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# JSONデータ読み込み
basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'store.json'), 'r', encoding='utf-8') as f:
    stores = json.load(f)


# ホーム確認用
@app.route("/")
def home():
    return "口コミAIツール：稼働中です！ /store/<id> にアクセスしてください"

# 各店舗ページ
@app.route("/store/<store_id>")
def store_page(store_id):
    store_data = next((s for s in stores if s["store_id"] == store_id), None)
    if not store_data:
        return "店舗が見つかりませんでした。", 404
    return render_template("store.html", store=store_data)

# 口コミ生成API
@app.route("/api/generate", methods=["POST"])
def generate_review():
    data = request.get_json()
    prompt = data.get("prompt")
    print("📥 プロンプト受信:", prompt)  # 追加

    if not prompt:
        return jsonify({"error": "プロンプトが空です"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは親しみやすく自然な日本語の口コミ文を作るアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=350
        )
        result = response.choices[0].message.content.strip()
        print("✅ 生成成功:", result)  # 追加
        return jsonify({"result": result})
    except Exception as e:
        print("❌ エラー内容:", e)  # 追加
        return jsonify({"error": str(e)}), 500


