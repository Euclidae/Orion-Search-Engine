from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__, template_folder='./static')

@app.route('/')
def home():
    return render_template('/web_search.html')

@app.route('/websearch', methods = ['GET', 'POST'])
def search():
    #get query from requests
    query = request.form['query']

    if query == "":
        render_template("web_search.html")

    #connect to the sqlite databae
    connection =  sqlite3.connect("crawled_pages.db")
    cursor = connection.cursor()

    #search for websites tha match the query in heir cleaned content
    cursor.execute("SELECT url, title FROM pages WHERE cleaned_content LIKE ? ORDER BY pagerank DESC", ('%' + query + '%',))
    urls = cursor.fetchall()

    connection.close()

    #render the urls that match the query
    return render_template('results.html', urls = urls, query = query)

if __name__ == "__main__":
    app.run(debug=True)