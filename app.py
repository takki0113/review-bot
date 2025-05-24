from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
import openai

# 環境変数の読み込み
load_dotenv()

# OpenAI APIキー設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask アプリ初期化
app = Flask(__name__)
CORS(app)

# store.json の読み込み
basedir = os.path.abspath(os.path.dirname(__file__))
store_path = os.path.join(basedir, 'store.json')
with open(store_path, 'r', encoding='utf-8') as f:
    stores = json.load(f)
print("✅ store.json 読み込み成功。全件数:", len(stores))


# ホームページ
@app.route("/")
def home():
    return "口コミAIツール：稼働中です！ /store/<id> にアクセスしてください"

# 店舗ページ表示
@app.route("/store/<store_id>")
def store_page(store_id):
    print(f"📍 リクエストされた store_id: {store_id}")
    store_data = next((s for s in stores if s["store_id"] == store_id), None)
    if not store_data:
        return "店舗が見つかりませんでした。", 404
    return render_template("store.html", store=store_data)


# 口コミ生成エンドポイント
@app.route("/api/generate", methods=["POST"])
def generate_review():
    data = request.get_json()
    prompt = data.get("prompt")
    print("📥 プロンプト受信:", prompt)

    if not prompt:
        return jsonify({"error": "プロンプトが空です"}), 400

    try:
        client = openai.OpenAI()  # ✅ 新スタイル
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
        print("✅ 生成成功:", result)
        return jsonify({"result": result})
    except Exception as e:
        print("❌ エラー内容:", e)
        return jsonify({"error": str(e)}), 500



# デバッグ実行用（Renderでは不要）
if __name__ == "__main__":
    app.run(debug=True)
