from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        prompt = f"請用繁體中文與英文各寫一句話摘要以下內容：{text}"

        try:
            result = summarizer(prompt, max_length=100, min_length=20, do_sample=False)
            summary = result[0]["summary_text"]
        except Exception as e:
            summary = f"發生錯誤：{str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
