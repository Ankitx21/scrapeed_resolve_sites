import requests
from bs4 import BeautifulSoup
from datetime import datetime

PROXIES_web = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
}

def verge_tech_convert_date(published):
    try:
        date_obj = datetime.strptime(published, "%b %d, %Y, %I:%M %p %Z")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return ""



def verge_tech_article_urls():
    base_url = "https://www.theverge.com"
    tech_url = f"{base_url}/tech"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'vmidv1=bc4a62af-a549-4def-8024-0fe2dddd4191; _chorus_geoip_continent=NA; _vm_consent_type=opt-out'
    }

    response = requests.get(tech_url, headers=headers, proxies=PROXIES_web, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs
    links = soup.find_all('a', class_='_1lkmsmo1')
    article_urls = [base_url + link['href'] for link in links if link.get('href')]

    return article_urls

def verge_tech_article_details(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'vmidv1=bc4a62af-a549-4def-8024-0fe2dddd4191; _chorus_geoip_continent=NA; _vm_consent_type=opt-out'
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', class_='_8enl991 _8enl990 _8enl996 _1xwticta _1xwtict9')
    title = title_tag.text.strip() if title_tag else ""

    # Scrape the author name and URL using the <span> and <a> tags
    author_span = soup.find('span', class_='_114qu8c2 _114qu8c3')
    author_tag = author_span.find('a') if author_span else None
    author_name = author_tag.text.strip() if author_tag else ""
    author_url = "https://www.theverge.com" + author_tag['href'] if author_tag else ""

    # Scrape the published date
# Extract published date
    published_tag = soup.find('span', class_='duet--article--timestamp')
    published = published_tag.get_text(strip=True) if published_tag else ''
    published_date = verge_tech_convert_date(published)


    # Scrape the article body
    body_tag = soup.find('div', class_='_1ymtmqpz')
    body = body_tag.text.strip() if body_tag else ""

    # Scrape author details
    author_details = verge_tech_author_details(author_url) if author_url else {}

    # Return the article details, including author details
    article_details = {
        "title": title,
        "author_name": author_name,
        "author_details": author_details,  # Include the author details dictionary
        "published": published,
        "published_date": published_date,
        "body": body,
    }

    return article_details

def verge_tech_author_details(author_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the author name
    author_name_tag = soup.find('h1', class_='duet--article--dangerously-set-cms-markup wh8b41p wh8b41l _1xwtict2 _1xwtict1')
    author_name = author_name_tag.text.strip() if author_name_tag else ''
    
    # Scrape the author image URL
    author_img_tag = soup.find('img', class_='_1f4081d5')
    author_img = author_img_tag['src'] if author_img_tag else ''
    
    # Placeholder for LinkedIn and Twitter
    author_linkedin = ''
# Extract author Twitter link
    twitter_tag = soup.find('a', class_='_1mu177r0', href=True)
    author_twitter = twitter_tag['href'] if twitter_tag else ''

    
    author_details = {
        "author_name": author_name,
        "author_img": author_img,
        "author_linkedin": author_linkedin,
        "author_twitter": author_twitter
    }
    
    return author_details

# Example usage
article_urls = verge_tech_article_urls()
print(article_urls)
for article_url in article_urls:
    article_details = verge_tech_article_details(article_url)
    if article_details:  # Only print if article details are not None
        print(article_details)
