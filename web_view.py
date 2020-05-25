import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from seen_movies import SeenMovie, thumbnail_exists, save_thumbnail
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from adapter import RemoteServerMovieClient, make_connection_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = make_connection_uri()

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
app.config['SECRET_KEY'] = FLASK_SECRET_KEY if FLASK_SECRET_KEY else 'thisisasupersecretkey'

class SeenMovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    year = IntegerField('year', validators=[DataRequired()])
    imdb = StringField('imdb')
    comment = StringField('comment')
    submit = SubmitField('submit')

@app.route('/', methods=['GET', 'POST'])
def showSeenMovies():
    form = SeenMovieForm()
    client = RemoteServerMovieClient()
    movies = client.get_all()

    if form.validate_on_submit():
        title = form.title.data
        year = form.year.data
        imdb = form.imdb.data
        comment = form.comment.data
        client.add(title=title, year=year, imdb=imdb, comment=comment)
        return redirect(url_for('showSeenMovies'))

    return render_template('seenmovies.html', form=form, movies=movies)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    client = RemoteServerMovieClient()
    movie_to_edit = client.get_by_id(id)
    movies = client.get_all()
    form = SeenMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        year = form.year.data
        imdb = form.imdb.data
        comment = form.comment.data
        client.update(movie_to_edit, title=title, year=year, imdb=imdb, comment=comment)
        return redirect(url_for('showSeenMovies'))

    return render_template('seenmovies.html', movie_to_edit=movie_to_edit, form=form, movies=movies)
