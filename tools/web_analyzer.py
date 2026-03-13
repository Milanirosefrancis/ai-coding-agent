import requests
from bs4 import BeautifulSoup


def analyze_webpage(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    return text[:5000]