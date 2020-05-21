"""
seenmovies.py: Keep track of movies watched in a SQL database
"""

import re
import requests
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, \
    MetaData, Table, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pathlib import Path

from datetime import datetime
from imdb import IMDb


# with engine.connect() as connection:
#     print(connection)
    # result = connection.execute("select * from seen")
    # for row in result:
    #     print(row)

Base = declarative_base()

class SeenMovie(Base):
    __tablename__ = 'seenmovies'

    id = Column(Integer(), primary_key=True)
    title = Column(String(200),nullable=False, unique=True)
    year = Column(Integer(), CheckConstraint('year>1894'))
    date_seen = Column(Date(), server_default=func.now())
    imdb = Column(String(20))
    comment = Column(Text())

    def __repr__(self):
        return f"{self.title} ({self.year}) seen: {self.date_seen}"

    def get_thumbnail_url(self):
        if not thumbnail_exists(self.title_slug()):
            ia = IMDb()
            movie = ia.get_movie(self.imdb)
            thumbnail_url = movie.get('cover url')
            save_thumbnail(self.title_slug(), thumbnail_url)

        return 'static/' + self.title_slug()

    def title_slug(self):
        return re.sub(r"[\s\.!\[\]\(\)\'\"]", '', self.title)



def find_movie_id_by_title_and_year(title, year):
    ia = IMDb()

    try:
        imdb_movie = next(x for x in ia.search_movie(title) if x.get('year') == year)
    except StopIteration:
        return None

    return imdb_movie.movieID

def get_director(imdb_id):
    movie = ia.get_movie(imdb_id)

    return movie.get('director')[0]['name']

def thumbnail_exists(name):
    f = Path('static/' + str(name))
    return f.is_file()

def save_thumbnail(name, url):
    img = requests.get(url).content
    with open('static/' + str(name), 'w+b') as f:
        f.write(img)

