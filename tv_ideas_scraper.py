# tv_ideas_scraper.py
import requests
from bs4 import BeautifulSoup
import random

def get_tv_ideas(symbol="BTCUSDT"):
    url_map = {
        "BTCUSDT": "https://www.tradingview.com/symbols/BTCUSDT/ideas/",
        "ETHUSDT": "https://www.tradingview.com/symbols/ETHUSDT/ideas/",
        "SOLUSDT": "https://www.tradingview.com/symbols/SOLUSDT/ideas/",
    }
    url = url_map.get(symbol)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    ideas = []
    for item in soup.select('div.js-idea-item')[:5]:
        title_tag = item.select_one('a.js-idea-title')
        author_tag = item.select_one('a.js-user-link')
        if title_tag and author_tag:
            title = title_tag.text.strip()
            link = "https://www.tradingview.com" + title_tag['href']
            author = author_tag.text.strip()
            sentiment = random.choice(['bullish', 'bearish', 'neutral'])
            ideas.append({
                "symbol": symbol,
                "title": title,
                "author": author,
                "link": link,
                "sentiment": sentiment
            })
    return ideas
