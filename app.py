import ast
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from newspaper import Article
from dotenv import load_dotenv
from insertToDB import pullFromDB

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
sourceList = ['cbc-news', 'cnn', 'bbc-news', 'reuters', 'associated-press']
sourceDict = {"CBC":'cbc-news', "CNN":'cnn', "BBC":'bbc-news' ,"Reuters":'reuters' ,"Associated Press":'associated-press'}

#This needs to be done on a daily basis 
# collectArticles(sourceList)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        sourceClean = request.form['sources']
        source = sourceDict[sourceClean]

        session["source"] = source
        # Prettier to display version of the source
        session["sourceClean"] = sourceClean

        return redirect(url_for("source"))
    else:
        return render_template("index.html")

@app.route("/source", methods=["POST", "GET"])
def source():
    if "source" in session and "sourceClean" in session:
        sourceClean = session["sourceClean"]
        source = session["source"]

        titles = pullFromDB(['title'], source)
        urls = pullFromDB(['url'], source)
        summaries = pullFromDB(['summary'], source)
        contents = pullFromDB(['content'], source)

        session["titles"] = titles
        session["urls"] = urls
        session["contents"] = contents

        return render_template("summary.html", source=sourceClean, titles=titles, urls=urls, summaries=summaries, contents=contents)
    else:
        return redirect(url_for("home"))

# Fix this, to make sure index is not being displayed as url
@app.route("/articleContent", methods=["POST", "GET"])
def articleContent():
    if request.method == "POST":
        # ast.eval() parses the dictionary inside the string, is safer than eval() 
        articleData = ast.literal_eval(request.form['articleData'])
        title = articleData['title']
        url = articleData['url']
        content = articleData['content']
        return render_template("articleContent.html", title=title, content=content, url=url)
    else:
        return redirect(url_for("home"))
if __name__ == "__main__":
    app.run(debug = True)