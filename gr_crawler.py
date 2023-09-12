import fetch_and_parse_html

URL = 'https://www.globalreinsurance.com/sections/news'

soup = fetch_and_parse_html.run(URL)

results = soup.find(id="news_5792")

more_news_URL = results.find("p", class_="more").find('a')['href']

news_elements = results.find_all("div", class_="subSleeve")

for news_element in news_elements:
    title_element = news_element.find("a")
    intro_element = news_element.find("p", class_="intro")
    url_element = title_element['href']
    print("Title: ", title_element.text.strip())
    print("Intro: ", intro_element.text.strip())
    print("URL: ", url_element)

    soup = fetch_and_parse_html.run(url_element)

    results = soup.find(id="wrapper_sleeve")

    article_date = results.find("p", class_="byline meta").text
    print("Date: ", article_date.strip("\n"))
    article_content = results.find("div", class_="storytext")
    article_content_elements = article_content.find_all("p")
    print("Content: ")
    for article_content_element in article_content_elements:
        print(article_content_element.text)
    print()

print(more_news_URL)

soup = fetch_and_parse_html.run(more_news_URL)

news_elements = soup.find_all("div", class_="listBlocks")
print(news_elements)