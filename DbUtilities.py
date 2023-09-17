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
    pool_size=10,
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

def get_id(url):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "SELECT id FROM news_articles WHERE url = %s"
    val = (url,)
    mycursor.execute(sql, val)

    article_id = mycursor.fetchone()
    return article_id
  except mysql.connector.Error as e:
    print(f"Error getting id: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def add_translation(id, title, content):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "INSERT INTO translated_articles (article_id, title, content) VALUES (%s, %s, %s)"
    val = (id, title, content)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "translated article inserted.")

  except mysql.connector.Error as e:
    print(f"Error adding translation: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def add_sentiment_analysis(id, sentiment, subjectivity):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "INSERT INTO sentiment_analysis (article_id, sentiment_score, subjectivity_score) VALUES (%s, %s, %s)"
    val = (id, sentiment, subjectivity)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "sentiment analysis inserted.")

  except mysql.connector.Error as e:
    print(f"Error adding sentiment analysis: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def add_reinsurer(ranking, company_name, glnl, nlnl, gnlo, nnlo, shareholders_fund, loss_ratio, expense_ratio, combined_ratio):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)
    sql = "INSERT INTO reinsurer_info (ranking, name, glnl, nlnl, gnlo, nnlo, shareholders_funds, loss_ratios, expense_ratios, combined_ratios) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (ranking, company_name, glnl, nlnl, gnlo, nnlo, shareholders_fund, loss_ratio, expense_ratio, combined_ratio)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "reinsurer inserted.")
  except mysql.connector.Error as e:
    print(f"Error adding reinsurer: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def link_reinsurer_to_article(article_id, reinsurer_id):
    try:
      connection = get_connection()
      mycursor = connection.cursor(buffered=True)
      # Check if the link already exists
      check_sql = "SELECT * FROM reinsurer_news_article_relationship WHERE reinsurer_id = %s AND article_id = %s"
      check_val = (reinsurer_id, article_id)
      mycursor.execute(check_sql, check_val)

      if mycursor.rowcount > 0:
          print("Reinsurer-article link already exists.")
      else:
          # If the link doesn't exist, insert it
          insert_sql = "INSERT INTO reinsurer_news_article_relationship (reinsurer_id, article_id) VALUES (%s, %s)"
          insert_val = (reinsurer_id, article_id)
          mycursor.execute(insert_sql, insert_val)
          connection.commit()
          print(mycursor.rowcount, "reinsurer linked to article.")

    except mysql.connector.Error as e:
      print(f"Error linking reinsurer to article: {str(e)}")
      raise
    finally:
      if connection:
        connection.close()

def get_reinsurer_list():
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "SELECT id, name FROM reinsurance_NLP.reinsurer_info"
    mycursor.execute(sql)

    reinsurer_list = mycursor.fetchall()
    return reinsurer_list
  except mysql.connector.Error as e:
    print(f"Error getting reinsurer list: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def add_category(name, description, keywords):
  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)
    sql = "INSERT INTO categories_info (name, description, keywords) VALUES (%s, %s, %s)"
    val = (name, description, keywords)

    mycursor.execute(sql, val)

    connection.commit()

    print(mycursor.rowcount, "category inserted.")
  except mysql.connector.Error as e:
    print(f"Error adding category: {str(e)}")
    raise
  finally:
    if connection:
      connection.close()

def link_category_to_article(article_id, category_id):
    try:
      connection = get_connection()
      mycursor = connection.cursor(buffered=True)
      # Check if the link already exists
      check_sql = "SELECT * FROM article_categories WHERE category_id = %s AND article_id = %s"
      check_val = (category_id, article_id)
      mycursor.execute(check_sql, check_val)

      if mycursor.rowcount > 0:
          print("Category-article link already exists.")
      else:
          # If the link doesn't exist, insert it
          insert_sql = "INSERT INTO article_categories (category_id, article_id) VALUES (%s, %s)"
          insert_val = (category_id, article_id)
          mycursor.execute(insert_sql, insert_val)
          connection.commit()
          print(mycursor.rowcount, "category linked to article.")

    except mysql.connector.Error as e:
      print(f"Error linking category to article: {str(e)}")
      raise
    finally:
      if connection:
        connection.close()

def get_categories():

  try:
    connection = get_connection()
    mycursor = connection.cursor(buffered=True)

    sql = "SELECT id, name, keywords FROM categories_info"
    mycursor.execute(sql)

    category_list = []
    
    rows = mycursor.fetchall()
    for row in rows:
        category_id, category_name, keywords_str = row
        keywords_list = keywords_str.split(',') if keywords_str else []
        category_list.append((category_id, category_name, keywords_list))

    return category_list

  except mysql.connector.Error as e:
    print(f"Error getting category list: {str(e)}")
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

def delete_all_articles():
    try:
      connection = get_connection()
      mycursor = connection.cursor(buffered=True)

      delete_sql = "DELETE FROM news_articles"
      mycursor.execute(delete_sql)
      
      connection.commit()

    except mysql.connector.Error as e:
        print(f"Error deleting all articles: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()