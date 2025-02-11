from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Intentionally allowing all origins (CORS issue)

def init_db():
    with sqlite3.connect("movies.db") as conn:
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

@app.route('/')
def index():
    return redirect(url_for('movies_list'))

@app.route('/movies')
def movies_list():
    with sqlite3.connect("movies.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
    return render_template("movies_list.html", movies=movies)

@app.route('/add_movie', methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        name = request.form['movie_name']
        director = request.form['director']
        cast = request.form['cast']
        rating = request.form['rating']
        description = request.form['description']

        with sqlite3.connect("movies.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movies (name, director, cast, rating, description) VALUES (?, ?, ?, ?, ?)",
                           (name, director, cast, rating, description))
            conn.commit()
        return redirect(url_for('movies_list'))

    return render_template("add_movie.html")

@app.route('/search_movie', methods=["GET"])
def search_movie():
    search = request.args.get('search')
    if search:
        with sqlite3.connect("movies.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM movies WHERE name LIKE '%{search}%'", ())  # SQL Injection vulnerability
            movies = cursor.fetchall()
        return render_template("movies_list.html", movies=movies)
    return redirect(url_for('movies_list'))

@app.route('/reviews/<int:movie_id>', methods=["GET", "POST"])
def movie_reviews(movie_id):
    with sqlite3.connect("movies.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM movies WHERE id=?", (movie_id,))
        movie_name = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM reviews WHERE movie_id=?", (movie_id,))
        reviews = cursor.fetchall()

    if request.method == "POST":
        review_text = request.form['review']  # XSS Vulnerability
        with sqlite3.connect("movies.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reviews (movie_id, review) VALUES (?, ?)", (movie_id, review_text))
            conn.commit()
        return redirect(url_for('movie_reviews', movie_id=movie_id))

    return render_template("movie_reviews.html", reviews=reviews, movie_name=movie_name, movie_id=movie_id)

@app.route('/openapi.json')
def openapi_spec():
    return send_file("openapi.json", mimetype="application/json")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
