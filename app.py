from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]

        try:
            result = summarizer(text, max_length=100, min_length=20, do_sample=False)
            summary = result[0]["summary_text"]
        except Exception as e:
            summary = f"發生錯誤：{str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
