import requests
from bs4 import BeautifulSoup
from datetime import datetime

def finsmes_articles_list():
    """Fetch all article URLs from the Finsmes homepage."""
    url = "https://www.finsmes.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all article links
    links = soup.find_all("h3", class_="entry-title td-module-title")

    # Extract URLs from <a> tags
    article_urls = [link.find("a")["href"] for link in links if link.find("a")]

    return article_urls

def finsmes_convert_date(published):
    """Convert published date string to structured format YYYY-MM-DD."""
    try:
        return datetime.strptime(published, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""  # Return empty string if format doesn't match

def finsmes_author_details():
    """Initialize author details fields as empty."""
    return {
        "author_name": "",
        "author_img": "",
        "author_twitter": "",
        "author_linkedin": ""
    }

def finsmes_article_details(article_url):
    """Fetch article details from a given Finsmes article URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.find("h1", class_="tdb-title-text")
    title = title_tag.text.strip() if title_tag else ""

    # Extract author name and link
    author_tag = soup.find("a", class_="tdb-author-name")
    author_name = author_tag.text.strip() if author_tag else ""
    author_link = author_tag["href"] if author_tag else ""

    # Extract published date
    published_tag = soup.find("time", class_="entry-date updated td-module-date")
    published = published_tag.text.strip() if published_tag else ""
    published_date = finsmes_convert_date(published)

    # Extract article body with paragraphs
    body_paragraphs = soup.find_all("div", class_="tdb-block-inner td-fix-index")

    # Get text from all paragraphs and join with spacing
    body = "\n\n".join([p.get_text(strip=True) for p in body_paragraphs])

    # Get author details
    author_details = finsmes_author_details()
    author_details["author_name"] = author_name
    author_details["author_link"] = author_link

    # Store the extracted data
    article_data = {
        "title": title,
        "published": published,
        "published_date": published_date,
        "body": body,
        "author_details": author_details
    }

    return article_data

def finsmes_scraper():
    """Scrape all articles from Finsmes homepage."""
    article_urls = finsmes_articles_list()
    articles_data = []

    for article_url in article_urls:
        article_data = finsmes_article_details(article_url)
        articles_data.append(article_data)

        # Print article details properly formatted
        print("\n" + "="*80)
        print(f"Title: {article_data['title']}")
        print(f"Author: {article_data['author_details']['author_name']} ({article_data['author_details']['author_link']})")
        print(f"Published: {article_data['published']}")
        print(f"Published Date: {article_data['published_date']}")
        print("\nArticle Body:\n")
        print(article_data['body'])
        print("="*80 + "\n")

    return articles_data

def finsmes_save():
    """Return all scraped articles with author details."""
    articles_data = finsmes_scraper()
    return {"articles": articles_data}

# Example usage
finsmes_save()
