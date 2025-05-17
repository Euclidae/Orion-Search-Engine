import networkx as nx
import sqlite3

#Connect to the sqlite databse
connection = sqlite3.connect('crawled_pages.db')
cursor = connection.cursor()

#retrieve all urls from database

cursor.execute("SELECT url FROM pages")
urls = [row[0] for row in cursor.fetchall()]

#empty directed graph
graph = nx.DiGraph()

#add nodes to the graph
for url in urls:
    graph.add_node(url)

#retrieve outgoing links of each websites from the database and add their edges
for url in urls:
    cursor.execute("SELECT outgoing_links FROM pages WHERE url = ?", (url,))
    outgoing_links = cursor.fetchone()[0].split(',')
    for link in outgoing_links:
        if link.startswith('http'):
            graph.add_edge(url,link)

#calculate page rank of the graph

page_rank = nx.pagerank(graph)

#store the pagerank scores in the database
for url in urls:
    cursor.execute("UPDATE page SET pagerank = ? WHERE url = ?",(page_rank[url],url))

#commit the changes
connection.commit()

connection.close()