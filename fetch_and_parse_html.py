import requests
import user_agents
from bs4 import BeautifulSoup

def run(url):
    try:
        page = requests.get(url, headers={'User-Agent': user_agents.random_agent()})
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the main page:", e)
        exit(1)

    return BeautifulSoup(page.content, "html.parser")
    