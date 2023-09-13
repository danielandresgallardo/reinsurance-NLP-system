import fetch_and_parse_html

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

    #date format = YYYYMMDDHHMMSS
    article_date = soup.find("p", class_="date").text
    article_date = article_date.split()
    article_date_tw = int(article_date[2] + month_to_digits[article_date[1]] + f"{int(''.join(filter(str.isdigit, article_date[0]))):02}" + "000000")
    #print("Date: ",article_date_tw)

    #If article is older than data on database
    if article_date_tw < last_date:
        return 1
    
    article_title = soup.find("div", id="articles-section").find('h1').text

    article_content = soup.find("div", class_="pf-content")
    article_content_elements = article_content.find_all("p")
    article_content = ""
    for article_content_element in article_content_elements:
        article_content += article_content_element.text
    
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