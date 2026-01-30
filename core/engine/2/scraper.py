import requests
from bs4 import BeautifulSoup
import time


def scrape_website(url, timeout=10):
    """Scrape headlines from a news website homepage"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = []

            for tag in soup.find_all(["h1", "h2", "h3", "a"], limit=50):
                text = tag.get_text(strip=True)
                if len(text) > 20 and len(text) < 200:
                    link = tag.get("href", "")
                    if link:
                        # Make absolute URL
                        if not link.startswith("http"):
                            if link.startswith("/"):
                                from urllib.parse import urlparse

                                parsed = urlparse(url)
                                link = f"{parsed.scheme}://{parsed.netloc}{link}"
                            else:
                                link = url.rstrip("/") + "/" + link

                        articles.append({"title": text, "link": link, "source": url})

            return articles

    except Exception as e:
        print(f"  Error scraping {url}: {str(e)[:50]}")
        return []

    return []


def scrape_all_sources(sources_list):
    """Scrape headlines from all sources"""
    print("Starting web scraping...")
    print(f"Total sources: {len(sources_list)}")
    print()

    all_articles = []

    for i, source in enumerate(sources_list, 1):
        print(f"[{i}/{len(sources_list)}] Scraping: {source}")
        articles = scrape_website(source)
        all_articles.extend(articles)
        print(f"  Found {len(articles)} headlines")
        time.sleep(1)

    print()
    print(f"Total headlines scraped: {len(all_articles)}")
    return all_articles


def format_scraped_content(articles):
    """Format scraped headlines for AI to verify"""
    if not articles:
        return "No articles found from web scraping."

    content = f"SCRAPED NEWS HEADLINES ({len(articles)} total):\n\n"

    for i, article in enumerate(articles[:100], 1):
        content += f"{i}. HEADLINE: {article['title']}\n"
        content += f"   LINK: {article.get('link', 'N/A')}\n"
        content += f"   SOURCE: {article['source']}\n\n"

    return content
