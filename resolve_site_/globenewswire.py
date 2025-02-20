import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import ProxyError, RequestException

# Proxy settings
PROXIES_web = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

GLOBENEWSWIRE_DOMAIN = "www.globenewswire.com"

def convert_date_format(date_str):
    date_part = date_str.split()[0:3]  # Extract date part
    date_str_cleaned = " ".join(date_part)
    try:
        date_obj = datetime.strptime(date_str_cleaned, "%B %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return ""

def globenewswire_article_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    url = "https://www.globenewswire.com/search/date/24HOURS/subject/fin"
    
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES_web, verify=False)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', {'data-section': 'article-url'})
        return ['https://www.globenewswire.com' + link.get('href') if not link.get('href').startswith('https') else link.get('href') for link in links]
    
    print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
    return None

def globenewswire_article_details(url):
    missing_fields = []

    try:
        response = requests.get(url, proxies=PROXIES_web, verify=False)
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find('h1', class_='article-headline')
    title = title_tag.text.strip() if title_tag else ""
    if not title:
        missing_fields.append("Title")

    published_tag = soup.find('time')
    published_text = published_tag.text.strip() if published_tag else ""
    published_date = ""
    if published_text:
        try:
            published_date = convert_date_format(published_text)
        except ValueError:
            published_date = ""
    else:
        missing_fields.append("Publish Date")

    author_tag = soup.find('span', class_='article-source')
    author_span = author_tag.find('a', itemprop='name') if author_tag else None
    author = author_span.text.strip() if author_span else ""
    if not author:
        missing_fields.append("Author")

    body_tag = soup.find('div', class_='main-body-container article-body')
    body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""
    if not body_content:
        missing_fields.append("Body Content")

    if not title or not published_date or not body_content:
        if missing_fields:
            print(f"Missing fields for {url}: {', '.join(missing_fields)}")
        return None

    return {
        'url': url,
        'title': title,
        'published': published_text,
        'published_date': published_date,
        'author': author,
        'body': body_content,
    }

def globenewswire_author_details():
    return {
        "author_name": "",
        "author_img": "",
        "author_twitter": "",
        "author_linkedin": ""
    }

def globenewswire_save():
    article_urls = globenewswire_article_list()
    if not article_urls:
        print("No articles found.")
        return

    for index, url in enumerate(article_urls, start=1):
        print(f"\n🔹 Fetching article {index}/{len(article_urls)}: {url}\n")

        article_data = globenewswire_article_details(url)
        if not article_data:
            continue

        author_data = globenewswire_author_details()

        print("=" * 80)
        print(f"URL: {article_data['url']}")
        print(f"Title: {article_data['title']}")
        print(f"Published: {article_data['published']} ({article_data['published_date']})")
        print(f"Author: {article_data['author']}")
        print(f"Body: {article_data['body'][:500]}...")  # Displaying only first 500 chars
        
        if author_data:
            print(f"\nAuthor Details:")
            print(f"Name: {author_data.get('author_name')}")
            print(f"Image: {author_data.get('author_img')}")
            print(f"Twitter: {author_data.get('author_twitter')}")
            print(f"LinkedIn: {author_data.get('author_linkedin')}")
        print("=" * 80 + "\n")

        # Sleep to mimic human-like browsing and avoid detection
        time.sleep(random.uniform(2, 5))  

# Run the scraper
globenewswire_save()
