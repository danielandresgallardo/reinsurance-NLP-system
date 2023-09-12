import requests
import user_agents
from bs4 import BeautifulSoup

URL = 'https://www.globalreinsurance.com/sections/news'

try:
    page = requests.get(URL, headers={'User-Agent': user_agents.random_agent()})
    page.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Error fetching the main page:", e)
    exit(1)

soup = BeautifulSoup(page.content, "html.parser")
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

    try:
        article_URL = requests.get(url_element, headers={'User-Agent': user_agents.random_agent()})
        article_URL.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the article page:", e)
        continue

    soup = BeautifulSoup(article_URL.content, "html.parser")
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
page = requests.get(more_news_URL, headers={'User-Agent': user_agents.random_agent()})

news_elements = results.find_all("div", class_="listBlocks")
print(news_elements)