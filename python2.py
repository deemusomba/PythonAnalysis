import requests
from bs4 import BeautifulSoup
import sqlite3
url = 'https://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movie_titles = []
movie_ratings = []

for movie in soup.select('td.titleColumn'):
    title = movie.select('a')[0].text
    movie_titles.append(title)

for rating in soup.select('td.posterColumn span[name="ir"]'):
    movie_ratings.append(float(rating['data-value']))

print(movie_titles)
print(movie_ratings)

conn = sqlite3.connect('movies.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS movies
             (id INTEGER PRIMARY KEY,
              title TEXT,
              rating REAL)''')

for i in range(len(movie_titles)):
    c.execute("INSERT INTO movies (id, title, rating) VALUES (?, ?, ?)",
              (i+1, movie_titles[i], movie_ratings[i]))

conn.commit()
conn.close()
conn = sqlite3.connect('movies.db')
c = conn.cursor()

c.execute('SELECT AVG(rating) FROM movies')
result = c.fetchone()

print('Average rating of the top 100 movies on IMDB:', result[0])

conn.close()

