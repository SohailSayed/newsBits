import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

#Create table
def createTable(cur):
        cur.execute('CREATE TABLE IF NOT EXISTS articleData (id SERIAL PRIMARY KEY,'
                                        'title varchar NOT NULL,'
                                        'source varchar NOT NULL,'
                                        'url varchar NOT NULL,'
                                        'content varchar NOT NULL,'
                                        'summary varchar(1000) NOT NULL,'
                                        'date_added date DEFAULT CURRENT_TIMESTAMP,'
                                        'date_published timestamp with time zone,'
                                        'imageURL varchar);'
                                        )

def insertToDB(title, source, url, content, summary, date_published, imageURL):
        try:

                load_dotenv()

                conn = psycopg2.connect(
                        host=os.getenv('HOST'),
                        database=os.getenv('DB_NAME'),
                        user=os.getenv('DB_USERNAME'),
                        password=os.getenv('DB_PASSWORD'))

                cur = conn.cursor()

                # If articleData table doesn't exist, create one
                createTable(cur)

                date_added = dt = datetime.now(timezone.utc)

                cur.execute('INSERT INTO articleData (title, source, url, content, summary, date_added, date_published, imageURL)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                        'ON CONFLICT (url) DO UPDATE '
                        'SET title = EXCLUDED.title, '
                        '    source = EXCLUDED.source, '
                        '    content = EXCLUDED.content, '
                        '    summary = EXCLUDED.summary,'
                        '    date_added = EXCLUDED.date_added,'
                        # '    date_published = EXCLUDED.date_published,'
                        '    imageURL = EXCLUDED.imageURL',
                        (title,
                        source,
                        url,
                        content,
                        summary,  
                        date_added,
                        imageURL)
                        )
                        # (title,
                        # source,
                        # url,
                        # content,
                        # summary,  
                        # date_published, 
                        # date_added,
                        # imageURL)
                        # )

                conn.commit()
                print('Article data has successfully been inserted')
                
                cur.close()
                conn.close()
        except Exception as e:
                print(e)

def pullFromDB(columnList, source=None):
        load_dotenv()

        conn = psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'))

        cur = conn.cursor()
        
        columns = ",".join(columnList)

        if source:
                query = "SELECT {0} FROM articleData WHERE date_added = CURRENT_DATE AND source = '{1}'".format(columns, source)
        else:
                query = "SELECT {} FROM articleData WHERE date_added = CURRENT_DATE".format(columns)
        
        cur.execute(query)
        pulledData = cur.fetchall()

        return pulledData

