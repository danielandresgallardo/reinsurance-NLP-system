import fetch_and_parse_html

def retrieve_data_from_article(url_element, last_date):

    #print("URL: ", url_element)
    
    soup = fetch_and_parse_html.run(url_element)

    #date format = YYYYMMDDHHMMSS
    article_date = soup.find("p", class_="byline meta").text
    #Remove characters except digits, convert to int
    article_date = int(''.join(filter(str.isdigit, article_date.strip("\n"))))
    #Convert date to Taiwan timezone
    article_date_tw = article_date//10000 - article_date%10000 + 800
    print("Date: ",article_date_tw)

    #If article is older than data on database
    if article_date_tw < last_date:
        return 1
    
    article_title = soup.find("div", class_="story_title").text
    print("Title: ", article_title.strip("\n"))

    article_intro = soup.find("div", class_="standfirst").text
    #print("Intro: ", article_intro)

    article_content = soup.find("div", class_="storytext")
    article_content_elements = article_content.find_all("p")
    #print("Content: ")
    #for article_content_element in article_content_elements:
        #print(article_content_element.text)
    #print()
    return 0

def update_news(last_date):
    
    URL = 'https://www.globalreinsurance.com/news/5792.more?navcode=1817'

    up_to_date = False

    while not up_to_date:
        soup = fetch_and_parse_html.run(URL)

        URL = soup.find("a", class_="next")['href']

        news_elements = soup.find_all("div", class_="storyDetails")

        for news_element in news_elements:
            url_element = news_element.find("h3").find("a")['href']
            if retrieve_data_from_article(url_element, last_date) == 1:
                up_to_date = True
                break
