import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime, timedelta

# Proxy & Headers Setup
proxy_res = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'
}

# List of User-Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

# ✅ Function to Convert Date
def times_of_israel_convert_date(published_str):
    """Converts a relative date string to an absolute date format (YYYY-MM-DD)."""
    
    today = datetime.today().date()  # Current date

    if "Today" in published_str:
        time_str = published_str.replace("Today, ", "").strip()
        dt = datetime.strptime(time_str, "%I:%M %p").time()
        return datetime.combine(today, dt).strftime("%Y-%m-%d")

    elif "Yesterday" in published_str:
        time_str = published_str.replace("Yesterday, ", "").strip()
        dt = datetime.strptime(time_str, "%I:%M %p").time()
        return datetime.combine(today - timedelta(days=1), dt).strftime("%Y-%m-%d")

    else:
        try:
            dt = datetime.strptime(published_str, "%B %d, %Y, %I:%M %p")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return ""

# ✅ Function to Get Article URLs
def times_of_israel_article_list():
    url = "https://www.timesofisrael.com/"
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers, proxies=proxy_res, verify=False, timeout=10)

        if response.status_code == 403:
            return []
        elif response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="headline")
        urls = [article.find("a")["href"] for article in articles if article.find("a")]

        return urls

    except requests.exceptions.RequestException as e:
        return []

# ✅ Function to Get Author Details
def times_of_israel_author_details(author_url):
    if author_url == "":
        return None

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    session = requests.Session()

    try:
        response = session.get(author_url, headers=headers, proxies=proxy_res, verify=False, timeout=10)

        if response.status_code == 403:
            print(f"403 Forbidden: Skipping author {author_url}")
            return None
        elif response.status_code != 200:
            print(f"Failed to fetch author page: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract author name
        name_tag = soup.find("h1", class_="name")
        author_name = name_tag.text.strip() if name_tag else "N/A"

 # Extract author image
        img_tag = soup.find("img", class_="writers-thumbnail")
        author_img = img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"


        # Extract author Twitter link
        twitter_tag = soup.find("li", class_="twitter")
        author_twitter = twitter_tag.find("a")["href"] if twitter_tag else "N/A"

        # Extract author LinkedIn link
        linkedin_tag = soup.find("li", class_="linkedin")
        author_linkedin = linkedin_tag.find("a")["href"] if linkedin_tag else "N/A"

        return {
            "author_name": author_name,
            "author_img": author_img,
            "author_twitter": author_twitter,
            "author_linkedin": author_linkedin
        }

    except requests.exceptions.RequestException as e:
        return None

# ✅ Function to Get Article Details
def times_of_israel_article_details(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }

    session = requests.Session()

    try:
        response = session.get(url, headers=headers, proxies=proxy_res, verify=False, timeout=10)

        if response.status_code == 403:
            print(f"403 Forbidden: Skipping {url}")
            return None
        elif response.status_code != 200:
            print(f"Failed to fetch article: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.find("h1", class_="headline")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract author and author URL
        author_tag = soup.find("a", class_="byline-link")
        author = author_tag.text.strip() if author_tag else "N/A"
        author_url = author_tag["href"] if author_tag else "N/A"

        # Extract published date
        date_tag = soup.find("span", class_="date")
        published_date_str = date_tag.text.strip() if date_tag else "N/A"
        published_date = times_of_israel_convert_date(published_date_str)

        # Extract article image
        image_tag = soup.find("a", rel="lightbox")
        article_image = image_tag["href"] if image_tag else "N/A"

        # Extract body text
        body_tag = soup.find("div", class_="the-content")
        body = body_tag.get_text(separator="\n").strip() if body_tag else "N/A"

        article_data = {
            "url": url,
            "title": title,
            "author": author,
            "author_url": author_url,
            "published" : published_date_str,
            "published_date": published_date,
            "article_image": article_image,
            "body": body
        }

        return article_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article {url}: {e}")
        return None

def times_of_israel_save(article_data, author_data):
    """Merges article details with author details into a single dictionary."""
    
    Articles = {
        "url": article_data.get("url", ""),
        "title": article_data.get("title", ""),
        "author": article_data.get("author", ""),
        "author_url": article_data.get("author_url", ""),
        "published": article_data.get("published", ""),
        "published_date": article_data.get("published_date", ""),
        "article_image": article_data.get("article_image", ""),
        "body": article_data.get("body", ""),
        "author_img": author_data.get("author_img", ""),
        "author_twitter": author_data.get("author_twitter", ""),
        "author_linkedin": author_data.get("author_linkedin", "")
    }
    
    return Articles


# ✅ Main Execution
if __name__ == "__main__":
    print("Fetching article URLs...")
    article_urls = times_of_israel_article_list()

    if not article_urls:
        print("No articles found.")
    else:
        for idx, url in enumerate(article_urls, start=1):
            print(f"\n🔹 Fetching article {idx}: {url}")
            article_data = times_of_israel_article_details(url)

            if article_data:
                print("\n✅ Article Details:")
                print("url:", article_data["url"])
                print("Title:", article_data["title"])
                print("Author:", article_data["author"])
                print("Author URL:", article_data["author_url"])
                print("published:", article_data["published"])
                print("Published Date:", article_data["published_date"])
                print("Article Image:", article_data["article_image"])
                print("Body Preview:", article_data["body"][:200])  # Print first 200 chars of body
                print("-" * 80)

                author_details = times_of_israel_author_details(article_data["author_url"])
                if author_details:
                    print("Author Image:", author_details["author_img"])
                    print("Author Twitter:", author_details["author_twitter"])
                    print("Author LinkedIn:", author_details["author_linkedin"])
                
                print("-" * 80)
            
            time.sleep(random.uniform(3, 6))
