import fetch_and_parse_html
import db_connector
from datetime import datetime
from googletrans import Translator

month_to_digits = {
    "January" : "01",
    "February" : "02",
    "March" : "03",
    "April" : "04",
    "May" : "05",
    "June" : "06",
    "July" : "07",
    "August" : "08",
    "September" : "09",
    "October" : "10",
    "November" : "11",
    "December" : "12"
}

def retrieve_data_from_article(url_element, last_date):
    soup = fetch_and_parse_html.run(url_element)

    #fetch date from website
    article_date = soup.find("p", class_="date").text

    #Convert to datetime
   # Convert to datetime
    article_date = article_date.strip()  # Remove leading/trailing spaces
    date_parts = article_date.split()
    day = date_parts[0].rstrip('thstndrd')  # Remove "th", "st", "nd", "rd" from the day
    month = date_parts[1]
    year = date_parts[2]
    formatted_date = f"{day} {month} {year}T00:00:00+0800"

    # Parse the date string
    article_date = datetime.strptime(formatted_date, '%d %B %YT%H:%M:%S%z')

    print(article_date)

    #Fetch author
    
    article_author = date_parts[5]+" "+date_parts[6]

    #If article is older than data on database
    if article_date == last_date:
        return 1
    
    #Convert to string format (%Y-%m-%dT%H:%M:%S%z)
    #article_date = article_date.strftime("%Y-%m-%dT%H:%M:%S%z")

    #Fetch title from website
    article_title = soup.find("div", id="articles-section").find('h1').text

    #Fetch content from website
    article_content = soup.find("div", class_="pf-content")
    article_content_elements = article_content.find_all("p")
    article_content = ""
    for article_content_element in article_content_elements:
        article_content += article_content_element.text
    
    db_connector.add_article(article_title, article_author, "Reinsurance News", article_date, article_content, url_element)


    translator = Translator()

    translated_title = translator.translate(article_title, dest='zh-tw').text

    translated_content = translator.translate(article_content, dest='zh-tw').text

    db_connector.add_translation(translated_title, translated_content)

    return 0



def update_news(last_date):
    
    URL = 'https://www.reinsurancene.ws/reinsurance-news/'

    up_to_date = False

    while not up_to_date:
        soup = fetch_and_parse_html.run(URL)

        URL = soup.find("a", class_="next page-numbers")['href']

        news_elements = soup.find_all("div", class_="col-9 pl-0")

        for news_element in news_elements:
            url_element = news_element.find("h3").find("a")['href']
            if retrieve_data_from_article(url_element, last_date) == 1:
                up_to_date = True
                break