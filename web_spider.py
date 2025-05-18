import requests
from bs4 import BeautifulSoup
import sqlite3
import subprocess
import os
import concurrent.futures  # Added for multithreading
#thank you to mr. pyGooner from discord (seriously, what's with that name) for helping mewith the back links thing
from urllib.parse import urlparse, urljoin  # Added urljoin for resolving links

def crawler(start_url, max_pages = 50):
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
    allowed_domain = None  # Will be set after first request (to handle redirects)

    while url_frontier and len(visited_pages) < max_pages:
        #DFS
        url = url_frontier.pop(0)
        if url in visited_pages:
            continue
        print(f"Crawling {url}")
       
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue
            
            # Set allowed_domain based on FINAL URL (after redirects)
            if allowed_domain is None:
                final_url = response.url
                allowed_domain = urlparse(final_url).netloc.lower()  # Normalize to lowercase
                print(f"Locking crawler to domain: {allowed_domain}")
                
            soup = BeautifulSoup(response.content, 'html.parser')
            title = ""
            if soup.find('title'):
                title = soup.find('title').string
            
            outgoing_links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if not href:
                    continue
                
                # Resolve relative URLs to absolute
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)
                
                # Normalize and check domain
                target_domain = parsed_url.netloc.lower()
                if target_domain != allowed_domain:  # Strict match (no subdomains)
                    continue  # Skip external domains
                
                outgoing_links.append(absolute_url)
                
                # Add to frontier if not already visited/queued
                if absolute_url not in visited_pages and absolute_url not in url_frontier:
                    url_frontier.append(absolute_url)
                    
            cursor.execute("INSERT OR REPLACE INTO pages (url, content, cleaned_content, title, outgoing_links) VALUES (?,?,?,?,?)", 
                          (url, str(soup), soup.get_text(), title, ','.join(outgoing_links)))
            connection.commit()
            visited_pages.add(url)  # this is a set, remember?
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            
    connection.close()
    print("Crawling complete.")
       
seed_urls = [
             "http://soulslore.wikidot.com/",
             "https://manual.cs50.io/",
             "https://bbc.co.uk/news/topics/c4y26wwj72zt",
             "https://www.cnn.com",
             "https://eldenring.fandom.com/wiki/Elden_Ring_Wiki"
             
]


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(crawler, seed_urls)

subprocess.call(["python", os.path.join(os.getcwd(), "pagerank.py")]) #automating calling the page ranking system. Maybe I should add the tokenizer, lementizer and other stuff. wait, I kinda did though
#TODO: Implemen stop words somewhere
#Update done. Stop, tokens and lemmy implemented in pagerank.py
#TODO make a terminal to make it easy for beginners to run thsi.. nah