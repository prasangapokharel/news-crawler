import requests
from bs4 import BeautifulSoup
import time


def read_article_content(url, timeout=20):
    """Read full article content from a news website or Facebook post"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        print(f"  Reading content from: {url[:70]}...")
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove unwanted elements
            for tag in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "header",
                    "footer",
                    "aside",
                    "iframe",
                    "advertisement",
                    "ads",
                ]
            ):
                tag.decompose()

            # Try multiple selectors for article content
            article_content = None

            # Common article selectors for news sites
            article_selectors = [
                {"name": "article"},
                {
                    "class_": [
                        "article-content",
                        "post-content",
                        "entry-content",
                        "story-content",
                        "news-content",
                        "content-body",
                        "article-body",
                        "main-content",
                    ]
                },
                {"id": ["article", "content", "main", "post"]},
            ]

            for selector in article_selectors:
                if "name" in selector:
                    article_content = soup.find(selector["name"])
                elif "class_" in selector:
                    for class_name in selector["class_"]:
                        article_content = soup.find("div", class_=class_name)
                        if article_content:
                            break
                elif "id" in selector:
                    for id_name in selector["id"]:
                        article_content = soup.find("div", id=id_name)
                        if article_content:
                            break

                if article_content:
                    break

            # If no article content found, try Facebook-specific selectors
            if not article_content or "facebook.com" in url:
                # Facebook post content
                fb_selectors = [
                    soup.find("div", {"data-ad-preview": "message"}),
                    soup.find("div", class_="userContent"),
                    soup.find("div", {"role": "article"}),
                ]
                for fb_content in fb_selectors:
                    if fb_content:
                        article_content = fb_content
                        break

            # Fallback to body
            if not article_content:
                article_content = soup.find("body")

            if article_content:
                # Extract all text from paragraphs, headings, and list items
                text_elements = article_content.find_all(
                    ["p", "h1", "h2", "h3", "h4", "li", "span", "div"]
                )

                text_parts = []
                for element in text_elements:
                    text = element.get_text(strip=True)
                    # Only include meaningful text (longer than 20 chars)
                    if len(text) > 20 and text not in text_parts:
                        text_parts.append(text)

                full_text = "\n".join(text_parts)

                # Limit to 3000 characters to avoid token overflow
                if len(full_text) > 3000:
                    full_text = full_text[:3000] + "...\n[Content truncated for length]"

                print(f"    Extracted {len(full_text)} characters")
                return full_text
            else:
                return "Could not extract article content from this page."

        else:
            return f"Error: HTTP {response.status_code}"

    except Exception as e:
        error_msg = f"Error reading article: {str(e)[:100]}"
        print(f"    {error_msg}")
        return error_msg


def read_all_matched_articles(matched_links):
    """Read full content from all matched article links"""
    print("\n-> Reading full articles from matched sources...")
    print(f"Total articles to read: {len(matched_links)}")
    print()

    articles_with_content = []

    for i, link_info in enumerate(matched_links, 1):
        url = link_info["link"]
        try:
            title_preview = (
                link_info["title"][:60].encode("ascii", "ignore").decode("ascii")
            )
            print(f"[{i}/{len(matched_links)}] Reading: {title_preview}...")
        except:
            print(f"[{i}/{len(matched_links)}] Reading article...")

        content = read_article_content(url)

        articles_with_content.append(
            {
                "title": link_info["title"],
                "link": url,
                "source": link_info["source"],
                "full_content": content,
            }
        )

        # Small delay between requests
        time.sleep(2)

    print()
    print(f"Completed reading {len(articles_with_content)} articles")
    return articles_with_content


def format_articles_for_ai(articles_with_content):
    """Format full articles for AI analysis"""
    if not articles_with_content:
        return "No articles to analyze."

    content = (
        f"FULL ARTICLES READ FROM SOURCES ({len(articles_with_content)} total):\n\n"
    )
    content += "=" * 80 + "\n\n"

    for i, article in enumerate(articles_with_content, 1):
        content += f"ARTICLE #{i}\n"
        content += f"TITLE: {article['title']}\n"
        content += f"LINK: {article['link']}\n"
        content += f"SOURCE: {article['source']}\n"
        content += f"\nFULL CONTENT:\n{article['full_content']}\n"
        content += "\n" + "=" * 80 + "\n\n"

    return content
