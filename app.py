import os
from flask import Flask, request, render_template
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    original_paragraphs = []
    if request.method == "POST":
        text = request.form["text"]
        original_paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        prompt = f"{text}\n\n請將上述內容直接摘要為繁體中文，只給我摘要本身，不需要任何標題、說明或多餘話語。"
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-001")
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"發生錯誤：{str(e)}"
    return render_template("index.html", summary=summary, original_paragraphs=original_paragraphs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  
    app.run(host="0.0.0.0", port=port)
