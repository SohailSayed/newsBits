import requests
import os
from newspaper import Article
from dotenv import load_dotenv
from summarizer import summarize_text
from insertToDB import insertToDB

def collectArticles(sourceList):
    load_dotenv()

    NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY')

    for source in sourceList:
        url = ('https://newsapi.org/v2/top-headlines?'
                    'sources={0}&'
                    'apiKey={1}'.format(source, NEWSAPI_API_KEY))

        response = requests.get(url)
        articles = response.json()['articles']
        
        for article in articles:
            try:
                title = article['title']
                url = article['url']

                articleData = Article(article['url'])
                articleData.download()
                articleData.parse()
                content = articleData.text

                summary = summarize_text(content, 130)
                
                if len(content) > 300:
                    insertToDB(title, source, url, content, summary)
            except:
                continue

sourceList = ['cbc-news', 'cnn', 'bbc-news', 'reuters', 'associated-press']
collectArticles(sourceList)