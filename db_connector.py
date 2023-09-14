import mysql.connector
from mysql.connector import pooling

mydb = {
  "host": "localhost",
  "user": "root",
  "password": "rootroot",
  "database": "reinsurance_NLP",
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="reinsurance_pool",
    pool_size=10,  # Adjust the pool size as needed
    **mydb,
)

def get_connection():
    try:
        connection = connection_pool.get_connection()
        return connection
    except mysql.connector.Error as e:
        print(f"Error getting a database connection: {str(e)}")
        raise


def fetch_last_date():
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)
    sql = "SELECT date FROM news_articles ORDER BY date DESC"
    mycursor.execute(sql)

    lastDate = mycursor.fetchone()
    
    if lastDate == None:
      return None
    else:
      return lastDate[0]
  except mysql.connector.Error as e:
    print(f"Error fetching last date: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()


def add_article(title, author, source, date, content, url):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)
    if author == 0:
      sql = "INSERT INTO news_articles (title, source, date, content, url) VALUES (%s, %s, %s, %s, %s)"
      val = (title, source, date, content, url)
    else:
      sql = "INSERT INTO news_articles (title, author, source, date, content, url) VALUES (%s, %s, %s, %s, %s, %s)"
      val = (title, author, source, date, content, url)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "article inserted.")
  except mysql.connector.Error as e:
    print(f"Error adding article: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()


def add_translation(title, content):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "SELECT id FROM news_articles WHERE title = %s"
    val = (title,)
    mycursor.execute(sql, val)

    article_id = mycursor.fetchone()

    sql = "INSERT INTO translated_articles (article_id, title, content) VALUES (%s, %s, %s)"
    val = (article_id, title, content)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "translated article inserted.")
  except mysql.connector.Error as e:
    print(f"Error adding translation: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()


def delete_old_articles(oldest_date):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "DELETE FROM news_articles WHERE date < (%s)"
    val = (oldest_date,)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "record(s) deleted")
  except mysql.connector.Error as e:
    print(f"Error deleting old articles: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def delete_all_data():
    try:
      connection = get_connection()
      mycursor = connection.cursor(buffered=True)
      
      tables_to_delete = ["news_articles", "translated_articles", "sentiment_analysis"]

      for table in tables_to_delete:
        delete_sql = f"DELETE FROM {table}"
        mycursor.execute(delete_sql)
      
        connection.commit()

        print(mycursor.rowcount, "record(s) deleted")
    except mysql.connector.Error as e:
        print(f"Error deleting all data: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()