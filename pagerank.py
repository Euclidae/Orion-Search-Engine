"""
- The PageRanker version... I lost count. Help.
- Now with 100% more regret about career choices
- If this breaks, light your computer on fire and blame SQLite (MySQL is cooler. Seriously what do you mean CREATE DATABASE doesn't work? Bro???)
- I am losing my sh**
- Massive improvement over original pagerank.py. You should know how to look at commit history, clown. Leave me alone.
"""

# --------------------------
# Imports (Dear God why so many)
# --------------------------
import sqlite3
import math
import re
import networkx as nx 
from nltk import word_tokenize, download as nltk_download  # Fuck you very much, NLP
from nltk.corpus import stopwords  # Because "the" and "and" aren't useful, apparently
from nltk.stem import WordNetLemmatizer  # Thanks ChatGPT for this line I don't understand
from time import sleep  # For pretending we care about DB locks (seriously, I hate these)
import nltk #jerry rigging this cuz of error. interpreter error said so uhhh...

# --------------------------
# Configuration 
# --------------------------
CUSTOM_STOPWORDS = ['click', 'go', 'dream', 'mongrel']  # Don't ask about 'mongrel'
DB_NAME = 'crawled_pages.db'  # Change this, whine that the search doesn't work and I'll find you
MAX_DB_RETRIES = 5  # Because SQLite loves to lock up when you breathe wrong

# --------------------------
# NLTK Setup (Updated to properly check for sentence tokenization)
# --------------------------
try:
    # Test both word and sentence tokenization
    word_tokenize('test sentence.')
    from nltk.tokenize import sent_tokenize
    sent_tokenize('Another test.')  # This checks for punkt... not the TV shoq
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk_download('punkt')
    nltk.download('punkt_tab') #Jerry Rigged with above.

try:
    stopwords.words('english')
except LookupError:
    print("Downloading stopwords...")
    nltk_download('stopwords')

try:
    WordNetLemmatizer().lemmatize('testing')
except LookupError:
    print("Downloading wordnet...")
    nltk_download('wordnet')

# --------------------------
# Database Stuff (AKA Pain Simulator). Thanks to the ugly homie BoyTheTall for all his SQL nonesense code. Might have borrowed some... things
# --------------------------
def get_db_connection():
    """Try to connect to DB without crying. Returns cursor or death. Thank god for no pointers"""
    attempts = 0
    while attempts < MAX_DB_RETRIES:
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.execute("PRAGMA busy_timeout = 5000")  # Magic number from StackOverflow
            return conn
        except sqlite3.OperationalError as e:
            print(f"Database locked! Attempt {attempts+1}. Error: {str(e)[:50]}...")
            sleep(1.5)
            attempts += 1
    raise RuntimeError("DB connection failed. Go home, everyone.")

# --------------------------
# PageRank Calculation (Where Math Happens)
# --------------------------
def calculate_pagerank():
    """Builds a graph of URLs and does magic Google math"""
    print("\n=== Starting PageRank ===")
    print("Building link graph (this better work)...")

    # Get URLs from DB
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM pages WHERE content IS NOT NULL") 
        urls = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(urls)} URLs. Let's get this bread.")

    # We make the graph
    # TODO speaking of graphs, make code neat later

    web = nx.DiGraph()
    web.add_nodes_from(urls)  # web graph built now we need to make it directed. like you love your mom and she loves you. Not like you like an OF girlfriend and
    #she doesn't like you back

    # Add edges for direction
    edge_count = 0
    for idx, url in enumerate(urls):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT outgoing_links FROM pages WHERE url = ?", (url,))
            links = cursor.fetchone()
        
       
        if links and links[0]:
            clean_links = [l.strip() for l in links[0].split(',') 
                          if l.startswith('http') and l in urls]
        else:
            clean_links = []

        # Add relationships (it's complicated)
        for link in clean_links:
            web.add_edge(url, link)
            edge_count += 1

        # Progress updates to feel alive
        if idx % 50 == 0:
            print(f"Processed {idx} URLs... {edge_count} edges (who cares?)")

    print(f"Final graph: {len(urls)} nodes, {edge_count} edges. Not terrible.")

    # Do the actual PageRank voodoo
    print("Calculating rankings (warning: math incoming)...")
    rankings = nx.pagerank(web, alpha=0.85)  # Warning: Messing with alpha values may summon PinkiePinkie

    # Save to DB before we regret everything
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for url, score in rankings.items():
            cursor.execute("UPDATE pages SET pagerank = ? WHERE url = ?", (score, url))
        conn.commit()
    
    print("PageRank done! Let's never do that again.\n")




# --------------------------
# Search Index (Where Hope Goes to Die)
# --------------------------
def build_search_index():
    """Builds TF-IDF index because regex search is for peasants - might as well let your cat roll on your keyboard, hey?"""
    print("\n=== Building Search Index ===")
    print("Initializing lemmatizer (thanks, ChatGPT)...")
    lemmatizer = WordNetLemmatizer()  # Magic word un-bastardizer. Pretty much returns words back their base state. tweaking -> tweak
    stop_words = set(stopwords.words('english')).union(CUSTOM_STOPWORDS)

    # Clear old index (goodbye, cruel data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM page_index")  # Nuclear option
        print("Old index nuked. Freedom!")

    # Get all documents (pray for memory. serious, watch how many pages you decide to insert into the spider.)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pages")
        total_docs = cursor.fetchone()[0]
        cursor.execute("SELECT url, title, cleaned_content FROM pages")
        pages = cursor.fetchall()

    print(f"Processing {len(pages)} pages. Make me a coffee...")

    # Track word appearances (big brother style)
    word_doc_counts = {}

    # Process each page (slowly, with regret)
    for idx, (url, title, content) in enumerate(pages):
        if not content:
            continue  

    
        text = "{} {} {}".format(title, title,content) if title else content

        # Tokenize and clean (the fun part)
        tokens = [
            lemmatizer.lemmatize(word.lower()) 
            for word in word_tokenize(text)
            if word.isalnum() and word not in stop_words and len(word) > 1
        ]

        # Count word frequencies (because someone has to)
        word_counts = {}
        for word in tokens:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Update document counts 
        for word in set(tokens):
            word_doc_counts[word] = word_doc_counts.get(word, 0) + 1

        # Insert into DB (cross your fingers)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for word, count in word_counts.items():
                cursor.execute("""
                    INSERT INTO page_index (word, url, frequency)
                    VALUES (?, ?, ?)
                """, (word, url, count))

        # Progress to maintain sanity
        if idx % 20 == 0:
            print(f"Processed {idx} docs... {len(word_counts)} unique words (kill me)")

    # TF-IDF Calculation (where mistakes happen)
    print("\nCalculating TF-IDF (prayer circle time)...")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT word FROM page_index")
        words = [row[0] for row in cursor.fetchall()]

        for word in words:
            docs_with_word = word_doc_counts.get(word, 1)  # Avoid division by zero (thanks, Satan)
            idf = math.log(total_docs / docs_with_word)
            
            cursor.execute("""
                UPDATE page_index
                SET tfidf = frequency * ?
                WHERE word = ?
            """, (idf, word))

        conn.commit()

    print("TF-IDF calculated! Results may vary.\n")

# --------------------------
# Main Execution 
# --------------------------
if __name__ == "__main__":
    calculate_pagerank()
    build_search_index()
    print("""\n
    Operation Complete!
    -------------------
    If it worked: You're welcome
    If it failed: I told you so
    """)
    
    # TODO: Add error handling (lol)
    # TODO: Remove swear words before showing to pushing to github
    # TODO: Figure out why Heracles keeps appearing in search results ... Update Done.``
    #now, replace some of the stuff here from that one Gilgamesh project...
    #yeah, who am I kidding? lol!
    #... this is why I don't have a girlfriend :_)``