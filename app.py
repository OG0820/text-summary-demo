from flask import Flask, request, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"請用繁體中文與英文摘要下列內容：\n{text}"

        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"發生錯誤：{str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
