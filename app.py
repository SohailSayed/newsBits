import ast
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from modules.insertToDB import pullFromDB

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

sourceList = ['cbc-news', 'cnn', 'bbc-news', 'reuters', 'associated-press']
sourceDict = {"CBC":'cbc-news', "CNN":'cnn', "BBC":'bbc-news' ,"Reuters":'reuters' ,"Associated Press":'associated-press'}

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if 'sources' in request.form:
            sourceClean = request.form['sources']
            source = sourceDict[sourceClean]

            # Prettier to display version of the source
            session["sourceClean"] = sourceClean

            return redirect(url_for("source", sourceName=source))
    return render_template("homepage.html")

@app.route("/source/<sourceName>", methods=["POST", "GET"])
def source(sourceName):
    if "sourceClean" in session:
        sourceClean = session["sourceClean"]
        source=sourceName

        titles = pullFromDB(['title'], source)
        urls = pullFromDB(['url'], source)
        summaries = pullFromDB(['summary'], source)
        contents = pullFromDB(['content'], source)
        imageURLs = pullFromDB(['imageURL'], source)
        datePublishedList = [date[0].strftime("%b %d %Y") for date in pullFromDB(['date_published'], source)]
        todaysDate = datetime.today().strftime("%A, %b %d, %Y")
        return render_template("summary.html", source=source, sourceClean=sourceClean, titles=titles, urls=urls, summaries=summaries, contents=contents, imageURLs=imageURLs, datePublishedList=datePublishedList,todaysDate=todaysDate)
    else:
        return redirect(url_for("home"))

@app.route("/source/<source>/<articleTitle>", methods=["POST", "GET"])
def articleContent(source, articleTitle):
    if request.method == "POST":
        # ast.eval() parses the dictionary inside the string, is safer than eval() 
        articleData = ast.literal_eval(request.form['articleData'])
        title = articleData['title']
        url = articleData['url']
        content = articleData['content'].split('\n')
        todaysDate = datetime.today().strftime("%A, %b %d, %Y")
        return render_template("articleContent.html", title=title, content=content, url=url, todaysDate=todaysDate)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)