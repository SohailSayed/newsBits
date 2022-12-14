import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
        host="localhost",
        database="bitesizednews",
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

cur = conn.cursor()

#Create table
def createTable():
        cur.execute('DROP TABLE IF EXISTS articleData;')
        cur.execute('CREATE TABLE articleData (id SERIAL PRIMARY KEY,'
                                        'title varchar NOT NULL,'
                                        'source varchar NOT NULL,'
                                        'url varchar NOT NULL,'
                                        'content varchar NOT NULL,'
                                        'summary varchar(1000) NOT NULL,'
                                        'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                        )

def insertToDB(title, source, url, content, summary):
#Insert data, sample right now
        try:
                load_dotenv()

                conn = psycopg2.connect(
                        host="localhost",
                        database="bitesizednews",
                        user=os.getenv('DB_USERNAME'),
                        password=os.getenv('DB_PASSWORD'))

                cur = conn.cursor()
                cur.execute('INSERT INTO articleData (title, source, url, content, summary)'
                        'VALUES (%s, %s, %s, %s, %s)',
                        (title,
                        source,
                        url,
                        content,
                        summary)
                        )

                conn.commit()
                print('data has successfully been inserted')
        except Exception as e:
                print(e)

cur.close()
conn.close()

