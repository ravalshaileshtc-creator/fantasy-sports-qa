import urllib.parse
import feedparser
import requests
from bs4 import BeautifulSoup

def fetch_trending_news(topic=None, limit=5):
    """
    Stage 1: News Scraper
    Fetches trending news articles via RSS feeds or Google News search.
    Returns a list of dicts with title, summary, link, source, and published date.
    """
    articles = []
    
    if topic and topic.strip():
        # Google News RSS search for specific topic
        encoded_topic = urllib.parse.quote(topic.strip())
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
    else:
        # Top technology / world news headlines
        rss_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:limit]:
            # Clean HTML from summary
            summary_clean = ""
            if 'summary' in entry:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                summary_clean = soup.get_text()

            articles.append({
                "title": entry.title,
                "summary": summary_clean or entry.title,
                "link": entry.link,
                "source": entry.get("source", {}).get("title", "Google News"),
                "published": entry.get("published", "")
            })
    except Exception as e:
        print(f"[NewsScraper] RSS error: {e}")

    # Fallback default items if fetch failed
    if not articles:
        articles.append({
            "title": f"Breaking Developments in {topic or 'Technology'}",
            "summary": f"Major announcements and innovations are reshaping the landscape of {topic or 'global tech'} today.",
            "link": "https://news.google.com",
            "source": "Tech News Daily",
            "published": "Just now"
        })

    return articles

if __name__ == "__main__":
    news = fetch_trending_news("Artificial Intelligence", limit=3)
    print(f"Scraped {len(news)} news items:")
    for idx, item in enumerate(news, 1):
        print(f"{idx}. {item['title']} ({item['source']})")
