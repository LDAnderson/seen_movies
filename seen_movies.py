"""
seenmovies.py: Keep track of movies watched in a SQL database
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, \
    MetaData, Table, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    title = Column(String(200),nullable=False)
    year = Column(Integer())
    date_seen = Column(Date(), default=datetime.now)
    imdb = Column(String(20))
    comment = Column(Text())

    def __repr__(self):
        return f"{self.title} ({self.year}) seen: {self.date_seen}"


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
