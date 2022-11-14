import requests
from transformers import pipeline
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "testkey"

def summarize_text(text: str, max_len: int) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    try:
        summary = summarizer(text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    except IndexError as ex:
        print(ex)
        return summarize_text(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        source = request.form['sources']
        session["source"] = source

        if source == "cbc":
            url = ('https://newsapi.org/v2/top-headlines?'
                'sources=cbc-news&'
                'apiKey=934c6a1a98ca46efa144a9957f555fdb')
            response = requests.get(url)
            parsedResponse = response.json()['articles']
            articleURL = parsedResponse[0]['url']
            title = parsedResponse[0]['title']
            session["articleURL"] = articleURL
            session["title"] = title
            r = requests.get(articleURL)
            soup = BeautifulSoup(r.content, 'html.parser')
            originalArticle = soup.find("div", class_ = "story").get_text()
            lent = len(originalArticle)

            summary = summarize_text(originalArticle, 130)

            session["summary"] = summary
        return redirect(url_for("source"))
    else:
        return render_template("index.html")

@app.route("/source")
def source():
    if "title" in session:
        title = session["title"]
    if "articleURL" in session:
        articleURL = session["articleURL"]
    if "source" in session:
        source = session["source"]
    if "summary" in session:
        summary = session["summary"]
        return render_template("summary.html", source = source, summary = summary, articleURL = articleURL, title=title)
        # return "<p>{0}</p>".format(summary)
    else:
        return redirect(url_for(home))

if __name__ == "__main__":
    app.run(debug = True)
    

