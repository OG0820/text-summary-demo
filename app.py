from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# 使用你的 Gemini API 金鑰
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API endpoint（Text-only model）
API_URL = f"https://generativelanguage.googleapis.com/v1beta1/models/gemini-pro:generateContent?key={API_KEY}"

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"請使用繁體中文與英文各寫一句話摘要下列內容：\n{text}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        try:
            response = requests.post(API_URL, json=payload)
            print("Raw Response:", response.text)
            result = response.json()
            summary = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            summary = f"發生錯誤：{str(e)}\n實際回應：{response.text}"
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
