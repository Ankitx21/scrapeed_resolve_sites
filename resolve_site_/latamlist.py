import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import ProxyError, RequestException

PROXIES_web = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

def convert_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return ""

def latamlist_article_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    url = "https://latamlist.com/"
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES_web, verify=False)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return latamlist_article_list()
    except RequestException as e:
        return None
    
    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('h2', class_='entry-title')
        for title in titles:
            link = title.find('a')
            if link:
                article_url = link.get('href')
                if article_url:
                    article_links.add(article_url)
        
        return article_links
    else:
        return None

def latamlist_author_details(author_url):
    """Extracts author details from the author's profile page."""
    try:
        response = requests.get(author_url, proxies=PROXIES_web, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract author name
            author_name_tag = soup.find('h1', class_='page-title')
            author_name = author_name_tag.text.strip() if author_name_tag else ""

            # Extract author image
            author_img_tag = soup.find('img', class_='avatar')
            author_img = author_img_tag.get('src') if author_img_tag else ""

            # Return author details with Twitter and LinkedIn as empty
            return {
                "author_name": author_name,
                "author_img": author_img,
                "author_twitter": "",
                "author_linkedin": ""
            }
        else:
            return None
    except ProxyError as e:
        print(f"Proxy error while fetching author details: {e}. Retrying...")
        time.sleep(5)
        return latamlist_author_details(author_url)
    except RequestException as e:
        print(f"Request failed for author details: {e}")
        return None

def latamlist_article_details(url):
    try:
        response = requests.get(url, proxies=PROXIES_web, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('h1', class_='entry-title')
            title = title.text.strip() if title else ""
            
            # Extract the author and author URL
            author_tag = soup.find('a', class_='url fn n')
            author = author_tag.text.strip() if author_tag else ""
            author_url = author_tag.get('href') if author_tag else ""

            # Extract published date
            published_tag = soup.find('li', class_='meta-date')
            published = published_tag.text.strip() if published_tag else ""
            publish_date = convert_date_format(published)
            
            # Extract body content
            body_tag = soup.find('div', class_='entry-content')
            body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""

            # Fetch author details if author URL is present
            author_details = latamlist_author_details(author_url) if author_url else {}

            # Combine article and author details
            return {
                'url': url,
                'title': title,
                'published': published,
                'publish_date': publish_date,
                'author': author,
                'author_url': author_url,
                'author_details': author_details,
                'body': body_content
            }
        else:
            return None
    except ProxyError as e:
        time.sleep(5)
        return latamlist_article_details(url)
    except RequestException as e:
        return None

def latamlist_save():
    """Fetches and saves articles along with author details."""
    total_article_links = latamlist_article_list()
    if total_article_links:
        for url in total_article_links:
            article_details = latamlist_article_details(url)
            if article_details:
                print(json.dumps(article_details, indent=4))
            time.sleep(random.uniform(2, 5))  # Random delay to mimic human browsing

# Run the scraper
latamlist_save()
