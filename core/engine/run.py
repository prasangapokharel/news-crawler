import sys
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE / "1"))
sys.path.insert(0, str(BASE / "2"))
sys.path.insert(0, str(BASE / "2" / "read"))
sys.path.insert(0, str(BASE / "3"))

import read
import execute
import response
import scraper
import source


def extract_sources_from_social(social_content):
    sources = []
    for line in social_content.split("\n"):
        if line.strip().startswith("- https://"):
            url = line.strip("- ").strip()
            sources.append(url)
    return sources


def extract_links_from_response(ai_response, articles):
    """Extract article links mentioned in AI response"""
    matched_links = []

    # Find all links in AI response
    link_pattern = r"https?://[^\s\)]+"
    found_links = re.findall(link_pattern, ai_response)

    # Match with original articles to get title and source
    for link in found_links:
        for article in articles:
            if article.get("link") == link or link in article.get("link", ""):
                matched_links.append(
                    {
                        "title": article["title"],
                        "link": article["link"],
                        "source": article["source"],
                    }
                )
                break

    # If no links found in response, take top 10 articles
    if not matched_links and articles:
        print("  No specific links in response, selecting top articles...")
        matched_links = [
            {"title": a["title"], "link": a["link"], "source": a["source"]}
            for a in articles[:10]
            if a.get("link", "").startswith("http")
        ]

    return matched_links


def run():
    print("=" * 60)
    print("NEPAL NEWS CRAWLER - DAILY EDITION")
    print("=" * 60)
    print()

    print("-> Layer 1: Reading system prompt...")
    system_prompt = read.get_system_prompt()

    social_file = BASE / "1" / "source" / "social" / "social.md"
    social_content = social_file.read_text(encoding="utf-8")
    news_sources = extract_sources_from_social(social_content)

    print(f"System prompt loaded")
    print(f"Found {len(news_sources)} news sources to scrape\n")

    print("-> Layer 2A: Scraping news websites...")
    print("(This may take several minutes...)")
    print()

    articles = scraper.scrape_all_sources(news_sources)
    scraped_content = scraper.format_scraped_content(articles)

    print()
    print("-> Layer 2B: AI verifying news from sources...")

    user_message = f"""You have been provided with {len(articles)} scraped news headlines with their source links below.

YOUR TASK:
1. Review EACH headline carefully
2. For headlines matching the focus keywords, note the:
   - Headline text
   - Source link
   - Which focus keyword it matches
3. Based on the headline, infer if there's a publication date or timeframe
4. Extract and report ONLY the news that matches priority topics

IMPORTANT:
- Focus on headlines containing the priority keywords from the system prompt
- Include the source link for each relevant news item
- If you can infer dates from headlines (like "today", "yesterday", dates), include them
- Organize by priority level

Provide a structured report with:
- Source name + Link
- Headline
- Brief analysis of why it matches
- Date/timeframe (if mentioned in headline)"""

    ai_response = execute.execute(system_prompt, user_message, scraped_content)
    print("AI preliminary analysis completed\n")

    # Extract matched article links from AI response
    print("-> Layer 2C: Reading full articles from matched sources...")
    matched_links = extract_links_from_response(ai_response, articles)

    if matched_links:
        print(f"Found {len(matched_links)} relevant articles to read in full")
        articles_with_content = source.read_all_matched_articles(matched_links)
        full_articles_text = source.format_articles_for_ai(articles_with_content)

        print("\n-> Layer 2D: AI final verification with full article content...")
        final_message = f"""Now you have the FULL CONTENT of relevant articles. 

Re-analyze these {len(articles_with_content)} articles with their complete text and provide:
1. Verify the news is actually about the focus topics (not just mentioned in passing)
2. Extract the publication date if available
3. Provide accurate summary based on full content
4. Confirm relevance and priority

Format each verified article with:
- Source + Link
- Publication Date
- Full headline
- Detailed summary from article content
- Why it matches focus priorities
- Priority level"""

        final_response = execute.execute(
            system_prompt, final_message, full_articles_text
        )
        print("AI final verification completed\n")
    else:
        print("No relevant articles found to read in full\n")
        final_response = ai_response

    print("-> Layer 3: Saving response...")
    file_path = response.save_response(final_response)
    print(f"Report saved: {file_path}\n")

    print("=" * 60)
    print("CRAWL COMPLETED SUCCESSFULLY")
    print("=" * 60)

    return final_response, file_path
