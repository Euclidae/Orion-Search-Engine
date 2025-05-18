**Orion Search Engine**  
*Explore web pages with less bloat*  

---
![image](https://github.com/user-attachments/assets/976a4217-96a6-4acd-bbcf-301fa405dc9c)

**🚀 What is this?**  
A retro-futuristic web crawler and search engine that feels like exploring a star map. Built with Python, SQLite, and Flask, featuring:  

- **Web spider** that crawls 10,000 pages (modify `max_pages` in `web_spider.py`)  
- **Cosmic-themed UI** with animated constellations and cyberpunk aesthetics  
- **PageRank algorithm** powering search results  
- **Self-contained database** (no cloud services required)  

Perfect for researchers, hobbyists, or anyone who wants to understand web crawling fundamentals without corporate tracking. Add your own websites to the seed_urls to expand and decrease search.

---

**🌌 Installation**  
*You’ll need:*  
- Python 3.10+  
- Basic terminal skills (i.e python source.py / python3 source.py)

1. Clone this repo:  
  ![image](https://github.com/user-attachments/assets/b3388b32-8467-4c1c-8d3b-bcb54e02c561)
![image](https://github.com/user-attachments/assets/c35f0b53-fd0d-406a-adb7-302f524a7249)


   ```bash
   git clone https://github.com/Euclidae/Orion-Search-Engine.git
   cd Orion-Search-Engine
   ```

3. Install requirements:  
![image](https://github.com/user-attachments/assets/472a5b80-d183-481a-a0c0-c55792cd6eb8)

   ```bash
   #requests should come in preinstalled but I have been told it sometimes doesn't.
   pip install requests beautifulsoup4 flask networkx
   ```

4. Start crawling (pick 1-2 seed URLs initially):  
   ```bash
   #run this first before you run web_search
   python web_spider.py
   ```

5. Calculate PageRank (run after crawling):  
   ```bash
   python pagerank.py
   ```

6. Launch the search portal:  
   ```bash
   # P.S I am apolitical so do not make assumptions based on my choice BBC. It was among the first to come to mind.
   python web_search.py
   ```

Visit `http://localhost:5000` on your web browser to begin exploring.  

---

**🔭 Key Components**  

1. **`web_spider.py`**  
   - Starts from seed URLs (BBC, CNN, CS50 Manual by default)  
   - Stores raw HTML and cleaned text in `crawled_pages.db`  
   - Avoids duplicate visits using URL frontier  

2. **`web_search.py`**  
   - Flask server with cyberpunk-themed templates  
   - Searches cleaned content using SQL LIKE queries  
   - Ranks results using pre-computed PageRank  

3. **`pagerank.py`**  
   - Builds link graph using NetworkX  
   - Updates PageRank scores in database  

4. **`static/`**  
   - Dark forest background image (`Forest-Dark.png`)  
   - CSS animations for constellation effects  
   - Retro terminal-style fonts  

---

**🌠 Customization**  
<u>web_spider.py</u>
![image](https://github.com/user-attachments/assets/f804e920-5dd6-43b9-982e-eb9c2c4849f1)

- **Add seed URLs**: Edit `seed_urls` in `web_spider.py`  
- **Change visual theme**: Modify `style.css` (try neon colors!)  
- **Improve ranking**: Adjust the PageRank damping factor in `pagerank.py`  
- **Add stopwords**: Cleaner content = better search results  

---

**🌍 Ethics & License**  
- *Use freely*: MIT License - modify, share, or build commercial projects  
- *Respect robots.txt*: Add parsing logic if crawling public sites  
- *Storage warning*: 10k pages ≈ 500MB local storage  

---

**📡 Troubleshooting**  

❗ *"Table pages has no column"*  
Delete `crawled_pages.db` and re-run the spider - schema updates require fresh DB.  

❗ *Slow crawling*  
Lower `max_pages` or add timeouts between requests.  

❗ *Missing constellation effects*  
Ensure Chrome/Firefox and hardware acceleration enabled.  

---

**🌌 Why "Orion"?**  
Named after the grand archer, Super Orion. I'd name it Gilgamesh, but that just sounds stupid, not gonna lie
https://typemoon.fandom.com/wiki/Super_Orion
https://typemoon.fandom.com/wiki/Gilgamesh
---

**🌕 Final Note**  
This isn’t Google - it’s a learning tool that prioritizes transparency over speed. Expect quirks, enjoy the retro vibe, and maybe add your own constellation patterns to the CSS.  

*May your searches always find starlight.*  

---  
Euclidae | 2024 | [GitHub](https://github.com/Euclidae)  
*Built with Python, insomnia, and a fascination with space-age retro*
