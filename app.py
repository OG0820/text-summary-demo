from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/uer/mt5-small-chinese-cluecorpussmall-summarization"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
}

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"請摘要以下內容：{text}"
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        try:
            summary = response.json()[0]["summary_text"]
        except Exception as e:
            summary = f"發生錯誤：{str(e)}\n原始回應：{response.text}"
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
