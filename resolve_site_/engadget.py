import requests
from bs4 import BeautifulSoup
from datetime import datetime

PROXIES_web = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

def engadget_article_urls():
    url = "https://www.engadget.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers, proxies=PROXIES_web, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    article_urls = []
    articles = soup.find_all('h4', class_='My(0)')

    for article in articles:
        link_tag = article.find('a')
        if link_tag and link_tag.get('href'):
            article_url = "https://www.engadget.com" + link_tag['href']
            article_urls.append(article_url)

    return article_urls

def engadget_convert_date(datetime_str):
    try:
        date_obj = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return "No date found"

def engadget_article_details(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch article {url}: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title found"
    
    author_tag = soup.find('span', class_='caas-author-byline-collapse')
    author_link = author_tag.find('a') if author_tag else None
    author = author_link.text.strip() if author_link else "No author found"
    author_url = author_link['href'] if author_link and author_link.has_attr('href') else "No author URL found"
    
    date_tag = soup.find('time')
    published_date_string = date_tag.text.strip() if date_tag else "No date string found"
    published_date = engadget_convert_date(date_tag['datetime']) if date_tag and date_tag.has_attr('datetime') else "No date found"
    
    body_tag = soup.find('div', class_='caas-body')
    body = " ".join([p.get_text(strip=True) for p in body_tag.find_all('p')]) if body_tag else "No body content found"
    
    return {
        "title": title,
        "url": url,
        "author": author,
        "author_url": author_url,
        "published_date": published_date,
        "published": published_date_string,
        "body": body,
    }

def engadget_author_details(author_url):
    if "No author URL found" in author_url:
        return {}
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(author_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch author details: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    author_img_tag = soup.find('img', class_='W(100px) H(100px) Bdrs(50%)')
    author_name = author_img_tag['alt'] if author_img_tag and 'alt' in author_img_tag.attrs else ""
    author_img = author_img_tag['src'] if author_img_tag and 'src' in author_img_tag.attrs else ""
    
    return {
        "author_name": author_name,
        "author_img": author_img,
        "author_twitter": "",
        "author_linkedin": ""
    }

def engadget_tech_save():
    article_urls = engadget_article_urls()
    if not article_urls:
        print("No articles found.")
        return
    
    for index, article_url in enumerate(article_urls, start=1):
        print(f"\n🔹 Fetching article {index}/{len(article_urls)}: {article_url}\n")
        
        article_data = engadget_article_details(article_url)
        if not article_data:
            continue
        
        author_data = engadget_author_details(article_data.get("author_url"))
        
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
    engadget_tech_save()
