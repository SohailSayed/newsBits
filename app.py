import requests
from transformers import pipeline
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "testkey"

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
            r = requests.get(articleURL)
            soup = BeautifulSoup(r.content, 'html.parser')
            originalArticle = soup.find("div", class_ = "story").get_text()

            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary = summarizer(originalArticle, max_length=130, min_length=30, do_sample=False)
            session["summary"] = summary[0]['summary_text']
        return redirect(url_for("source"))
    else:
        return render_template("index.html")

@app.route("/source")
def source():
    # if "source" in session:
    #     source = session["source"]
    #     return "<h1>You have selected {source}</h1>".format(source)
    if "summary" in session:
        summary = session["summary"]
        return "<p>{0}</p>".format(summary)
    else:
        return redirect(url_for(home))

if __name__ == "__main__":
    app.run(debug = True)
    

