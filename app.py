import requests
from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for, session
from newspaper import Article

app = Flask(__name__)
app.secret_key = "testytest"

def summarize_text(text: str, max_len: int) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    try:
        summary = summarizer(text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    # Might need to specify this exception to handle IndexError and tensorflow.python.framework.errors_impl.InvalidArgumentError somehow (second one is hard, gotta figure out)
    except:
        return summarize_text(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        source = request.form['sources']
        session["source"] = source

        if source == "cbc":
            # Everything below probably needs to be made into a seperate function soon
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=cbc-news&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
            response = requests.get(url)
            parsedResponse = response.json()['articles']

            titles = []
            urls = []
            for article in parsedResponse:
                titles.append(article['title'])
                urls.append(article['url'])
            session["titles"] = titles
            session["urls"] = urls
        return redirect(url_for("source"))
    else:
        return render_template("index.html")

@app.route("/source", methods=["POST", "GET"])
def source():
    if "titles" in session:
        titles = session["titles"]
    if "urls" in session:
        urls = session["urls"]
    if "source" in session:
        source = session["source"]
        if request.method == "POST":
            articleURL = request.form["articleURL"]
            articleData = Article(articleURL)
            articleData.download()
            articleData.parse()
            articleText = articleData.text
            
            summary = summarize_text(articleText, 130)
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=summary, articleURL=articleURL)
        else:
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=False)
    else:
        return redirect(url_for(home))

if __name__ == "__main__":
    app.run(debug = True)
    

