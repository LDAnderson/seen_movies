from flask import Flask, render_template, request, redirect, url_for
from seen_movies import SeenMovie
from client import SeenMovieClient

app = Flask(__name__)

@app.route('/')
def showSeenMovies():
    client = SeenMovieClient("SQLAlchemy")
    movies = client.seen()
    return render_template('seenmovies.html', movies=movies)
