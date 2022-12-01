import requests
from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for, session
from newspaper import Article
from rq import Queue

app = Flask(__name__)
app.secret_key = "testytest"
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def summarize_text(text: str, max_len: int) -> str:
    try:
        summary = query({"inputs" : text, "max_length" : max_len,})
        return summary[0]["summary_text"]
    except:
        return summarize_text(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        source = request.form['sources']
        session["source"] = source

        #This is a rudimentary way of calling the selected source, must be changed soon
        if source == "CBC":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=cbc-news&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
        if source == "CNN":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=cnn&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
        if source == "BBC":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=bbc-news&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
        if source == "Reuters":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=reuters&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
        if source == "Associated Press":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=associated-press&'
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
            
            # summary = summarize_text(articleText, 130)
            summary = summarize_text(articleText, 130)
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=summary, articleURL=articleURL)
        else:
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=False)
    else:
        return redirect(url_for(home))

if __name__ == "__main__":
    app.run(debug = True)
    

