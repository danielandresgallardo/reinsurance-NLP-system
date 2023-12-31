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
        article_date = soup.find("p", class_="byline meta").text.strip()

        #Convert to datetime
        article_date = article_date[-25:-3]+article_date[-2:]
        article_date = datetime.strptime(article_date, '%Y-%m-%dT%H:%M:%S%z')

        #If article is older than data on database, exit
        if article_date < last_date:
            return 1
        
        #Convert datetime to string format (%Y-%m-%dT%H:%M:%S%z)
        article_date = article_date.strftime("%Y-%m-%dT%H:%M:%S%z")

        #Fetch title from website
        article_title = soup.find("div", class_="story_title").text

        article_content = soup.find("div", class_="standfirst").text

        #Fetch content from website
        article_temp = soup.find("div", class_="storytext")
        article_content_elements = article_temp.find_all("p")
        for article_content_element in article_content_elements:
            article_content += article_content_element.text
        
        DbUtilities.add_article(article_title, 0, "Global Reinsurance", article_date, article_content, url_element)

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
    
    URL = 'https://www.globalreinsurance.com/sections/news'
    
    soup = fetch_and_parse_html.run(URL)

    URL = soup.find("p", class_="more").find("a")['href']

    up_to_date = False

    while not up_to_date:
        try:
            soup = fetch_and_parse_html.run(URL)

            URL = soup.find("a", class_="next")['href']

            news_elements = soup.find_all("div", class_="storyDetails")
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
