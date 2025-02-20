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
        date_obj = datetime.strptime(date_str, "%b %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return ""

def global_venturing_article_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    url = "https://globalventuring.com/sectors/startups/"
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES_web, verify=False)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return global_venturing_article_list()
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a', class_='mt-2 bigNewsLink w-100 d-inline-block'):
            article_url = link.get('href')
            if article_url:
                if not article_url.startswith('https'):
                    article_url = 'https://globalventuring.com' + article_url
                article_links.add(article_url)
                
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def global_venturing_article_details(url):
    try:
        response = requests.get(url, proxies=PROXIES_web, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1')
            title = title_tag.text.strip() if title_tag else ""

            # Extract author and published date
            author_tag = soup.find('h4', class_='lineTitle')
            if author_tag:
                author_span = author_tag.find('span')
                if author_span:
                    author_text = author_span.text.strip()
                    published_date_str = author_text.split('•')[0].strip()
                    author = author_text.split('•')[1].strip() if '•' in author_text else ""
                    published = published_date_str
                    publish_date = convert_date_format(published_date_str)
                else:
                    author, published, publish_date = "", "", ""
            else:
                author, published, publish_date = "", "", ""

            # Extract body content
            body_tag = soup.find('div', class_='hiddenWrap')
            body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""

            return {
                'url': url,
                'title': title,
                'published': published,
                'publish_date': publish_date,
                'author': author,
                'body': body_content
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return global_venturing_article_details(url)
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

def global_venturing_author_details():
    return {
        "author_name": "",
        "author_img": "",
        "author_twitter": "",
        "author_linkedin": ""
    }

def global_venturing_save():
    article_urls = global_venturing_article_list()
    if not article_urls:
        print("No articles found.")
        return

    for index, article_url in enumerate(article_urls, start=1):
        print(f"\n🔹 Fetching article {index}/{len(article_urls)}: {article_url}\n")

        article_data = global_venturing_article_details(article_url)
        if not article_data:
            continue

        author_data = global_venturing_author_details()

        print("=" * 80)
        print(f"URL: {article_data['url']}")
        print(f"Title: {article_data['title']}")
        print(f"Published: {article_data['published']} ({article_data['publish_date']})")
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

if __name__ == "__main__":
    global_venturing_save()
