import requests
import os
from transformers import pipeline
from flask import Flask, render_template, request, redirect, url_for, session
from newspaper import Article
from dotenv import load_dotenv
from tasks import summarize

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer {}".format(os.getenv('INFERENCE_API_KEY'))}
NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY')

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
                'apiKey={}'.format(NEWSAPI_API_KEY))
        if source == "CNN":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=cnn&'
                'apiKey={}'.format(NEWSAPI_API_KEY))
        if source == "BBC":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=bbc-news&'
                'apiKey={}'.format(NEWSAPI_API_KEY))
        if source == "Reuters":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=reuters&'
                'apiKey={}'.format(NEWSAPI_API_KEY))
        if source == "Associated Press":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=associated-press&'
                'apiKey={}'.format(NEWSAPI_API_KEY))
        
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
            
            summary = summarize.delay(articleText, 130)
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=summary, articleURL=articleURL)
        else:
            return render_template("summary.html", source=source, titles=titles, urls=urls, summary=False)
    else:
        return redirect(url_for(home))

@app.route("/<title>", methods=["POST", "GET"])
def articleContent(title):
    if request.method == "POST":
        articleURL = request.form["articleURL"]
        articleData = Article(articleURL)
        articleData.download()
        articleData.parse()
        articleText = articleData.text.split('\n')
        return render_template("articleContent.html", title=title, articleText=articleText, articleURL=articleURL)
if __name__ == "__main__":
    app.run(debug = True)
    

