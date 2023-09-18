# reinsurance-NLP-system

NPL analysis system for international reinsurance news at Cathay Property Insurance. This system will collect and process news data, provide translations, and offer user-friendly access.

## Table of Contents

- [Project Description](#project-description)
- [Requirements](#requirements)
- [Usage](#usage)
- [Future improvements](#future-improvements)

## Project Description

Python application built using the Flask web framework. It functions as a reinsurance news data scraper and inquiry tool, incorporating natural language processing (NLP) to extract sentiment and subjectivity scores from news articles. The application also allows users to sort news articles by categories, reinsurer, and news source.

### Features

1. **Web Framework (Flask)**:
   - Utilizes the Flask web framework to create a user-friendly web application for accessing reinsurance news data.

2. **Database Connection**:
   - Establishes a connection to a MySQL database named "reinsurance_nlp_db" with customizable connection parameters.

3. **Homepage**:
   - Root route ('/') renders an 'index.html' template, likely serving as the application's homepage.

4. **News Listing**:
   - '/news' route displays a list of news articles.
   - Users can optionally filter articles by specifying a 'category.'
   - Articles are fetched from the database based on the selected category and displayed using the 'news.html' template.

5. **Article Details**:
   - '/article/<int:article_id>' route shows detailed information about a specific news article identified by its 'article_id.'
   - Retrieves information about associated reinsurers, sentiment analysis scores, and the translated article's title and content from the database.
   - Conducts sentiment analysis and classifies sentiment as Positive, Negative, or Neutral.
   - Renders article details using the 'article.html' template.

6. **Search Functionality**:
   - '/search' route provides a search interface for filtering news articles based on criteria such as category, reinsurer, and source.
   - Processes search parameters submitted via a form (POST request).
   - Constructs SQL queries based on selected search parameters and retrieves matching articles from the database.
   - Displays search results using the 'search_results.html' template.
   - Fetches and displays available categories and reinsurers for filtering.

7. **Database Queries**:
   - Executes SQL queries to retrieve data from the database, including article details, category information, reinsurer data, sentiment scores, and search results.

8. **Bootstrap Integration**:
   - Integrates the Flask-Bootstrap extension to enhance the visual appearance and styling of web pages.

9. **Server Configuration**:
   - Utilizes the Waitress server to serve the Flask app on '127.0.0.1' at port '8080.'
   - The 'app.run' line (commented) can be used for development purposes.

### Screenshots/Demo

![Screenshot01](images/Screenshot01.png)

Link to demo: [Demo](http://danielgallardo.pythonanywhere.com/)

## Requirements

python3.11
flask
libraries

## Usage

## Future Improvements