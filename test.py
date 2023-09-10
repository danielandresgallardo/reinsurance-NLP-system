import requests
import random
from bs4 import BeautifulSoup


user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

URL = 'https://www.globalreinsurance.com/sections/news'
page = requests.get(URL, headers={'User-Agent': random.choice(user_agents_list)})

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="news_5792")

job_elements = results.find_all("div", class_="subSleeve")
for job_element in job_elements:
    title_element = job_element.find("a")
    intro_element = job_element.find("p", class_="intro")
    url_element = title_element['href']
    print("Title: ",title_element.text.strip())
    print("Intro: ",intro_element.text.strip())
    print("URL :",url_element)
    print()
