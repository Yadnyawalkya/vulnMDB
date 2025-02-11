import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    director TEXT NOT NULL,
                    cast TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    description TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_id INTEGER,
                    review TEXT,
                    FOREIGN KEY(movie_id) REFERENCES movies(id)
                )''')

conn.commit()
conn.close()
