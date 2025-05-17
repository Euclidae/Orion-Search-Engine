import requests
from bs4 import BeautifulSoup
import sqlite3
def crawler(start_url, max_pages = 10000):
    connection = sqlite3.connect('crawled_pages.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS pages")
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS pages(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT UNIQUE,
                   content TEXT,
                   cleaned_content TEXT,
                   title TEXT,
                   outgoing_links TEXT,
                   pagerank REAL
                   )
""")
    connection.commit()
    url_frontier = [start_url]
    visited_pages = set()
    while url_frontier and len(visited_pages) < max_pages:
        url = url_frontier.pop(0)
        if url in visited_pages:
            continue
        print(f"Crawling {url}")
       
        response = requests.get(url)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find('title'):
            title = soup.find('title').string
        outgoing_links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                outgoing_links.append(href)
        cursor.execute("INSERT OR REPLACE INTO pages (url, content, cleaned_content, title, outgoing_links) VALUES (?,?,?,?,?)", (url,str(soup),soup.get_text(), title,','.join(outgoing_links)))
        connection.commit()
        links = soup.find_all('a')
        for link in links:
            href = link.get("href")
            if href and (href.startswith("http://") or href.startswith("https://")):
                url_frontier.append(href)
        visited_pages.add(url)#this is a set, remember?
    connection.close()
    print("Crawling complete.")
       
seed_urls = [
             "https://manual.cs50.io/",
             "https://bbc.co.uk/news/topics/c4y26wwj72zt",
             "https://www.cnn.com",
             
]
for url in seed_urls:
    crawler(url)