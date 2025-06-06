import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"{text}\n\n請將上述內容直接摘要為繁體中文，只給我摘要本身，不需要任何解釋、標題或說明文字。"
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-001")
            response = model.generate_content(prompt)
            summary = response.text  
        except Exception as e:
            summary = f"發生錯誤：{str(e)}"
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
