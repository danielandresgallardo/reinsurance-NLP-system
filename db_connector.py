import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="reinsurance_NLP"
)

def fetch_last_date():
  mycursor = mydb.cursor(buffered=True)
  sql = "SELECT date FROM news_articles ORDER BY date DESC"
  mycursor.execute(sql)

  lastDate = mycursor.fetchone()
  
  if lastDate == None:
    return None
  else:
    return lastDate[0]



def add_article(title, author, source, date, content, url):
  mycursor = mydb.cursor(buffered=True)
  if author == 0:
    sql = "INSERT INTO news_articles (title, source, date, content, url) VALUES (%s, %s, %s, %s, %s)"
    val = (title, source, date, content, url)
  else:
    sql = "INSERT INTO news_articles (title, author, source, date, content, url) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (title, author, source, date, content, url)

  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "article inserted.")

def add_translation(title, content):
  mycursor = mydb.cursor(buffered=True)

  sql = "SELECT id FROM news_articles WHERE title = %s"
  val = (title,)
  mycursor.execute(sql, val)

  article_id = mycursor.fetchone()

  sql = "INSERT INTO translated_articles (article_id, title, content) VALUES (%s, %s, %s)"
  val = (article_id, title, content)

  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "translated article inserted.")



def delete_old_articles(oldest_date):

  mycursor = mydb.cursor(buffered=True)

  sql = "DELETE FROM news_articles WHERE date < (%s)"
  val = (oldest_date,)

  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "record(s) deleted")

def delete_all_data():
    mycursor = mydb.cursor(buffered=True)
    
    tables_to_delete = ["news_articles", "translated_articles", "sentiment_analysis"]

    try:
        for table in tables_to_delete:
            delete_sql = f"DELETE FROM {table}"
            mycursor.execute(delete_sql)
    
        mydb.commit()

        print(mycursor.rowcount, "record(s) deleted")
    except Exception as e:
        mydb.rollback()  # Rollback changes in case of an error
        print(f"Error deleting data: {str(e)}")
    finally:
        mycursor.close()  # Close the cursor