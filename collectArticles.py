import requests
import os
from newspaper import Article
from dotenv import load_dotenv
# Change this to not import summarize_text in the future from app.py
from app import summarize_text
from insertToDB import insertToDB

load_dotenv()

NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY')

sourceList = ['cbc-news', 'cnn', 'bbc-news', 'reuters', 'associated-press']

for source in sourceList:
    url = ('https://newsapi.org/v2/top-headlines?'
                'sources={0}&'
                'apiKey={1}'.format(source, NEWSAPI_API_KEY))

    response = requests.get(url)
    articles = response.json()['articles']
    
    if source == 'cnn':
        for article in articles:
            title = article['title']
            url = article['url']

            articleData = Article(article['url'])
            articleData.download()
            articleData.parse()
            content = articleData.text

            summary = summarize_text(content, 130)

            insertToDB(title, source, url, content, summary)