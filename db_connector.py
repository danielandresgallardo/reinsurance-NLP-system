import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="reinsurance_NLP"
)

def fetch_last_date():
  mycursor = mydb.cursor()

  sql = "SELECT date FROM news_articles ORDER BY date DESC"

  mycursor.execute(sql)

  lastDate = mycursor.fetchone()
  return lastDate

def add_article(title, source, date, content, url):
  mycursor = mydb.cursor()

  sql = "INSERT INTO news_articles (title, source, date, content, url) VALUES (%s, %s, %s, %s, %s)"
  val = (title, source, date, content, url)
  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "article inserted.")

def delete_old_articles(oldest_date):

  mycursor = mydb.cursor()

  sql = "DELETE FROM news_articles WHERE date < (%s)"
  val = (oldest_date,)

  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "record(s) deleted")

#add_article("title test", "Test source", 20230911000000, "test content", "test url")
#print(fetch_last_date())