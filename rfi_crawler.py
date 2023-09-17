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
        article_date = soup.find("time")["datetime"]

        #Convert to datetime
        article_date = datetime.strptime(article_date, '%Y-%m-%dT%H:%M:%S%z')

        #If article is older than data on database, exit
        if article_date < last_date:
            return 1
        
        #Convert datetime to string format (%Y-%m-%dT%H:%M:%S%z)
        article_date = article_date.strftime("%Y-%m-%dT%H:%M:%S%z")


        #Fetch author
        article_author = soup.find("a", class_="m-from-author__name").text


        #Fetch title from website
        article_title = soup.find("h1", class_="a-page-title").text

        #Fetch content from website
        article_content = soup.find("div", class_="t-content__body u-clearfix")
        article_content_elements = article_content.find_all("p")
        article_content = ""
        for article_content_element in article_content_elements:
            article_content += article_content_element.text
        
        DbUtilities.add_article(article_title, article_author, "rfi", article_date, article_content, url_element)

        article_id = DbUtilities.get_id(url_element)
        print(len(url_element))

        if article_id is not None:
            translated_title, translated_content = TranslationUtilities.translate_to_english(article_title, article_content)
            TextAnalysisUtilities.Analyze_text(article_id[0], translated_title, translated_content)
            DbUtilities.link_category_to_article(article_id[0], 5)
        else:
            print("No matching article found for translating and analyzing.")


        return 0
    except Exception as e:
        print(f"Error processing article: {str(e)}")
        return 1

def update_news(last_date):
    
    URL = 'https://www.rfi.fr/tw/%E9%97%9C%E9%8D%B5%E8%A9%9E/%E8%87%AA%E7%84%B6%E7%81%BD%E5%AE%B3/'

    page_num = 1

    up_to_date = False

    while not up_to_date:
        try:
            print("NEXT PAGEEEEEEEEEEEEEEEEEEEEE")
            soup = fetch_and_parse_html.run(URL)

            page_num += 1

            #next page
            URL = "https://www.rfi.fr/tw/%E9%97%9C%E9%8D%B5%E8%A9%9E/%E8%87%AA%E7%84%B6%E7%81%BD%E5%AE%B3/"+str(page_num)+"/#pager"

            news_elements = soup.find_all("div", class_="m-item-list-article")
            # Create a ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Create a list of futures by submitting tasks
                futures = []
                
                for news_element in news_elements:
                    url_element = "https://www.rfi.fr/" + news_element.find("a")['href']
                    future = executor.submit(retrieve_data_from_article, url_element, last_date)
                    futures.append(future)
                
                for future in concurrent.futures.as_completed(futures):
                    if future.result() == 1:
                        up_to_date = True
                        break

        except Exception as e:
            print(f"Error updating news: {str(e)}")
