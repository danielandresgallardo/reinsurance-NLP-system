import requests
import random
from bs4 import BeautifulSoup

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/99.0.999.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    # Add more User-Agent strings here
]

URL = 'https://www.globalreinsurance.com/sections/news'

try:
    page = requests.get(URL, headers={'User-Agent': random.choice(user_agents_list)})
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
        article_URL = requests.get(url_element, headers={'User-Agent': random.choice(user_agents_list)})
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
page = requests.get(more_news_URL, headers={'User-Agent': random.choice(user_agents_list)})

news_elements = results.find_all("div", class_="listBlocks")
print(news_elements)