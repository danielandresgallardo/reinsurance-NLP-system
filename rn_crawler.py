import fetch_and_parse_html
import DbUtilities
from datetime import datetime
import concurrent.futures
import TranslationUtilities
import TextAnalysisUtilities

def retrieve_data_from_article(url_element, last_date):
    try:
        soup = fetch_and_parse_html.run(url_element)

        #fetch date from website
        article_date = soup.find("p", class_="date").text

        #Convert to datetime
        article_date = article_date.strip()  # Remove leading/trailing spaces
        date_parts = article_date.split()
        day = date_parts[0].rstrip('thstndrd')  # Remove "th", "st", "nd", "rd" from the day
        month = date_parts[1]
        year = date_parts[2]
        formatted_date = f"{day} {month} {year}T00:00:00+0800"

        # Parse the date string
        article_date = datetime.strptime(formatted_date, '%d %B %YT%H:%M:%S%z')
        
        #If article is older than data on database
        if article_date < last_date:
            return 1
        
        #Fetch author
        
        article_author = date_parts[5]+" "+date_parts[6]

        #Convert to string format (%Y-%m-%dT%H:%M:%S%z)
        article_date = article_date.strftime("%Y-%m-%dT%H:%M:%S%z")

        #Fetch title from website
        article_title = soup.find("div", id="articles-section").find('h1').text

        #Fetch content from website
        article_content = soup.find("div", class_="pf-content")
        article_content_elements = article_content.find_all("p")
        article_content = ""
        for article_content_element in article_content_elements:
            article_content += article_content_element.text
        
        DbUtilities.add_article(article_title, article_author, "Reinsurance News", article_date, article_content, url_element)

        article_id = DbUtilities.get_id(url_element)

        if article_id is not None:
            TranslationUtilities.translate_and_upload(article_id[0], article_title, article_content)
            TextAnalysisUtilities.Analyze_text(article_id[0], article_title, article_content)
        else:
            print("No matching article found for translating and analyzing.")


        return 0
    except Exception as e:
        print(f"Error processing article: {str(e)}")
        return 1


def update_news(last_date):
    
    URL = 'https://www.reinsurancene.ws/reinsurance-news/'

    up_to_date = False

    while not up_to_date:
        try:
            soup = fetch_and_parse_html.run(URL)

            URL = soup.find("a", class_="next page-numbers")['href']

            news_elements = soup.find_all("div", class_="col-9 pl-0")
            # Create a ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Create a list of futures by submitting tasks
                futures = []

                for news_element in news_elements:
                    url_element = news_element.find("h3").find("a")['href']
                    future = executor.submit(retrieve_data_from_article, url_element, last_date)
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    if future.result() == 1:
                        up_to_date = True
                        break
        except Exception as e:
            print(f"Error updating news: {str(e)}")