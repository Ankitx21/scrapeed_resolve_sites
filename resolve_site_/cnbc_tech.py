import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

PROXIES_web = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

def cnbc_tech_convert_date(published_text):
    try:
        match = re.search(r'([A-Za-z]+ \d{1,2} \d{4})', published_text)
        if not match:
            raise ValueError("Date format not found in text")
        
        date_part = match.group(1)  
        formatted_date = datetime.strptime(date_part, "%b %d %Y").strftime("%Y-%m-%d")
        return formatted_date
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None

def cnbc_tech_article_urls():
    url = "https://www.cnbc.com/technology/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "region=WORLD;"
    }

    response = requests.get(url, headers=headers, proxies=PROXIES_web, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    article_urls = [a['href'] for a in soup.find_all('a', class_='Card-title') if a.get('href') and a['href'].startswith("https://www.cnbc.com")]

    return article_urls

def cnbc_tech_article_details(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "region=WORLD;"
    }

    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the article: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_='ArticleHeader-headline')
    title = title_tag.text.strip() if title_tag else None

    time_tag = soup.find('time', {"data-testid": "published-timestamp"})
    published = time_tag.text.strip() if time_tag else None
    published_date = time_tag['datetime'].split('T')[0] if time_tag and 'datetime' in time_tag.attrs else None
    formatted_published_date = cnbc_tech_convert_date(published) if published else None

    author_tag = soup.find('div', class_='Author-authorNameAndSocial')
    author_name = author_tag.find('a', class_='Author-authorName').text.strip() if author_tag and author_tag.find('a', class_='Author-authorName') else None
    author_url = author_tag.find('a', class_='Author-authorName')['href'] if author_tag and author_tag.find('a', class_='Author-authorName') else None

    body = " ".join([p.get_text(strip=True) for p in soup.select('div.group p')])

    return {
        "url": article_url,
        "title": title,
        "published": published,
        "published_date": formatted_published_date,
        "author": author_name,
        "author_url": author_url,
        "body": body
    }

def cnbc_tech_author_details(author_url):
    if not author_url:
        return {}

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "region=WORLD;"
    }

    response = requests.get(author_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch author details: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')

    author_name_tag = soup.find('h1', class_='RenderBioDetails-name')
    author_name = author_name_tag.text.strip() if author_name_tag else None

    author_img_tag = soup.find('div', class_='RenderBioDetails-image').find('img') if soup.find('div', class_='RenderBioDetails-image') else None
    author_img = author_img_tag['src'] if author_img_tag else None

    twitter_tag = soup.find('a', class_='icon-social_twitter')
    author_twitter = twitter_tag['href'] if twitter_tag else None

    linkedin_tag = soup.find('a', class_='icon-social_linkedin')
    author_linkedin = linkedin_tag['href'] if linkedin_tag else None

    return {
        "author_name": author_name,
        "author_img": author_img,
        "author_twitter": author_twitter,
        "author_linkedin": author_linkedin
    }

def cnbc_tech_save():
    article_urls = cnbc_tech_article_urls()
    if not article_urls:
        print("No articles found.")
        return

    for index, article_url in enumerate(article_urls, start=1):
        print(f"\n🔹 Fetching article {index}/{len(article_urls)}: {article_url}\n")
        
        article_data = cnbc_tech_article_details(article_url)
        if not article_data:
            continue
        
        author_data = cnbc_tech_author_details(article_data.get("author_url"))
        
        print("=" * 80)
        print(f"URL: {article_data['url']}")
        print(f"Title: {article_data['title']}")
        print(f"Published: {article_data['published']} ({article_data['published_date']})")
        print(f"Author: {article_data['author']} ({article_data['author_url']})")
        print(f"Body: {article_data['body'][:500]}...")  
        
        if author_data:
            print(f"\nAuthor Details:")
            print(f"Name: {author_data.get('author_name')}")
            print(f"Image: {author_data.get('author_img')}")
            print(f"Twitter: {author_data.get('author_twitter')}")
            print(f"LinkedIn: {author_data.get('author_linkedin')}")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    cnbc_tech_save()
