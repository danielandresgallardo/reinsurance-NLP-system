from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configure the database connection
db = mysql.connector.connect(
  host="localhost",
  user= "root",
  password= "rootroot",
  database= "reinsurance_nlp_db",
)
cursor = db.cursor()

# Define a route for the homepage with top navigation bar
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the "News" page to display a list of articles
@app.route('/news')
@app.route('/news/<category>')
def news(category=None):
    if category:
        cursor.execute("SELECT article_id FROM article_categories WHERE category_id = %s", (category,))
        articles_id = cursor.fetchall()
        placeholders = ', '.join(['%s'] * len(articles_id))
        cursor.execute("SELECT article_id, title FROM translated_articles WHERE article_id IN ({placeholders})",articles_id)
    else:
        cursor.execute("SELECT article_id, title FROM translated_articles")
    articles = cursor.fetchall()

    return render_template('news.html', articles=articles, selected_category=category)

@app.route('/article/<int:article_id>')
def article(article_id):
    # Fetch the list of reinsurer IDs associated with the article
    cursor.execute("SELECT reinsurer_id FROM reinsurer_news_article_relationship WHERE article_id = %s", (article_id,))
    reinsurer_id_rows = cursor.fetchall()

    reinsurer_ids = []
    for row in reinsurer_id_rows:
        reinsurer_ids.append(row)
    # Fetch reinsurer data based on the list of IDs
    reinsurer_data = []
    if reinsurer_ids != "":
        for reinsurer_id in reinsurer_ids:
            cursor.execute("SELECT * FROM reinsurer_info WHERE id = %s", (reinsurer_id[0],))
            reinsurer_info = cursor.fetchone()
            if reinsurer_info:
                reinsurer_data.append(reinsurer_info)
        print(reinsurer_data)
        # Fetch the article data
        cursor.execute("SELECT * FROM news_articles WHERE id = %s", (article_id,))
        article = list(cursor.fetchone())
        print(article)
    
    cursor.execute("SELECT sentiment_score, subjectivity_score FROM sentiment_analysis WHERE article_id = %s", (article_id,))
    sentiment_data = cursor.fetchall()
    sentiment_data = sentiment_data[0]
    sentiment_data = [round(sentiment_data[0]*100),'',round(sentiment_data[1]*100)]

    if sentiment_data[0] > 25:
        sentiment_data[1] = 'Positive'
    elif sentiment_data[0] < -25:
        sentiment_data[1] = 'Negative'
    else:
        sentiment_data[1] = 'Neutral'
    

    cursor.execute("SELECT title, content FROM translated_articles WHERE article_id = %s", (article_id,))
    translated = cursor.fetchone()

    article[1] = translated[0]
    article[5] = translated[1]

    return render_template('article.html', article=article, reinsurer_data=reinsurer_data, sentiment_data=sentiment_data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Retrieve search parameters from the form
        category = request.form.get('category')
        reinsurer = request.form.get('reinsurer')
        source = request.form.get('source')  # Get the source parameter

        # Create and execute SQL query based on search parameters
        query = "SELECT article_id, title FROM translated_articles WHERE 1=1"
        if category:
            query += f" AND article_id IN (SELECT article_id FROM article_categories WHERE category_id = '{category}')"
        if reinsurer:
            query += f" AND article_id IN (SELECT article_id FROM reinsurer_news_article_relationship WHERE reinsurer_id = '{reinsurer}')"
        if source:
            query += f" AND article_id IN (SELECT id FROM news_articles WHERE source = '{source}')"

        cursor.execute(query)
        search_results = cursor.fetchall()
        return render_template('search_results.html', results=search_results, category=category, reinsurer=reinsurer, source=source)

    # Retrieve the list of available categories
    cursor.execute("SELECT id, name FROM categories_info")
    categories = cursor.fetchall()

    # Retrieve the list of available reinsurers
    cursor.execute("SELECT id, name FROM reinsurer_info")
    reinsurers = cursor.fetchall()

    return render_template('search.html', categories=categories, reinsurers=reinsurers)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)
    #app.run(port=8080, debug=True) #for development
