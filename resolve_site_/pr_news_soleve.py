import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
import random
from requests.exceptions import ProxyError, RequestException

# Proxy settings
PROXIES_Data = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

def prnewswire_article_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    url = "https://www.prnewswire.com/news-releases/financial-services-latest-news/financing-agreements-list/"
    
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES_Data, verify=False)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return prnewswire_article_list()
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_links = set()

        links = soup.find_all('a', class_='newsreleaseconsolidatelink display-outline w-100')
        for link in links:
            article_url = link.get('href')
            if article_url:
                if not article_url.startswith('https'):
                    article_url = 'https://www.prnewswire.com' + article_url
                article_links.add(article_url)

        return article_links

    print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
    return None

def prnewswire_article_details(url):
    try:
        response = requests.get(url, proxies=PROXIES_Data, verify=False)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return prnewswire_article_details(url)
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else 'Title not found'

        published_tag = soup.find('p', class_='mb-no')
        published_str = ''
        published = ''
        if published_tag:
            try:
                published_str = published_tag.get_text(strip=True).split(',')[0] + ' ' + published_tag.get_text(strip=True).split(',')[1].strip().split(' ')[0]
                published = datetime.strptime(published_str, '%b %d %Y').strftime('%m/%d/%Y')
            except ValueError:
                published = 'Date parsing error'

        body_div = soup.find('div', class_='col-lg-10 col-lg-offset-1')
        body = body_div.get_text(separator='\n', strip=True) if body_div else 'Body not found'

        author_div = soup.find('div', class_='col-lg-8 col-md-8 col-sm-7 swaping-class-left')
        author_tag = author_div.find('strong') if author_div else None
        author = author_tag.get_text(strip=True) if author_tag else 'Author not found'

        author_link_tag = author_div.find('a') if author_div else None
        author_url = 'https://www.prnewswire.com' + author_link_tag['href'] if author_link_tag and author_link_tag.get('href') else None

        article_data = {
            'url': url,
            'title': title,
            'published': published_str,
            'published_date': published,
            'author': author,
            'author_url': author_url,
            'body': body,
        }

        print("\n===== Article Extracted =====")
        for key, value in article_data.items():
            print(f"{key}: {value}")
        print("============================\n")

        return article_data

    print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
    return None

def prnewswire_author_details():
    """ Returns an empty author details dictionary as per request. """
    author_details = {
        'author_name': '',
        'author_img': '',
        'author_twitter': '',
        'author_linkedin': '',
    }

    print("\n===== Author Extracted =====")
    for key, value in author_details.items():
        print(f"{key}: {value}")
    print("============================\n")

    return author_details

def prnewswire_save():
    article_urls = prnewswire_article_list()
    if not article_urls:
        print("No articles found.")
        return

    for url in article_urls:
        article_data = prnewswire_article_details(url)
        if article_data:
            author_details = prnewswire_author_details()
        time.sleep(random.uniform(2, 5))  # Introduce delay to avoid detection

# Run the scraper
prnewswire_save()
