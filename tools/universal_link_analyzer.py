import requests
from bs4 import BeautifulSoup
import re


def analyze_link(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string if soup.title else ""

    text = soup.get_text()

    clean_text = re.sub(r"\s+", " ", text)

    result = f"""
TITLE:
{title}

CONTENT:
{clean_text[:5000]}
"""

    return result