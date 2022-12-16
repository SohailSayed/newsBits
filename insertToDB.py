import psycopg2
import os
from dotenv import load_dotenv

#Create table
def createTable(cur):
        cur.execute('CREATE TABLE IF NOT EXISTS articleData (id SERIAL PRIMARY KEY,'
                                        'title varchar NOT NULL,'
                                        'source varchar NOT NULL,'
                                        'url varchar NOT NULL,'
                                        'content varchar NOT NULL,'
                                        'summary varchar(1000) NOT NULL,'
                                        'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                        )

def insertToDB(title, source, url, content, summary):
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

                cur.execute('INSERT INTO articleData (title, source, url, content, summary)'
                        'VALUES (%s, %s, %s, %s, %s)',
                        (title,
                        source,
                        url,
                        content,
                        summary)
                        )

                conn.commit()
                print('Article data has successfully been inserted')
                
                cur.close()
                conn.close()
        except Exception as e:
                print(e)



