from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from seen_movies import SeenMovie, Base

DB_USER = "myapp"
DB_PASS = "dbpass"
DB_HOST = "127.0.0.1"
DB_PORT = "15432"
DB_NAME = "movies_seen"

def make_connection_uri(host=DB_HOST, port=DB_PORT, username=DB_USER,
                        pw=DB_PASS, dbname=DB_NAME, database='postgres'):
    if database == 'postgres':
        connection_string = "postgresql+psycopg2://" + \
        username + ':' + pw + '@' + host + ':' + port + '/' + dbname
    else:
        raise NotImplementedError()
    return connection_string

class SQLAlchemyAdapter():
    def __init__(self):
        self.engine = create_engine(make_connection_uri())
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_movies(self):
        return self.session.query(SeenMovie).all()

    def add(self, title=None, year=None, date_seen=None, imdb=None, comment=None):
        if imdb.startswith('tt'):
            imdb = imdb[2:]

        seen_movie = SeenMovie(
            title = title,
            year = year,
            date_seen = date_seen,
            imdb = imdb,
            comment = comment)
        self.session.add(seen_movie)
        self.session.commit()

    def get(self, title):
        return self.session.query(SeenMovie).filter_by(title=title).one()

    def get_by_id(self, id):
        return self.session.query(SeenMovie).filter_by(id=id).one()

    def update(self, movie, **kwargs):
        for attribute, value in kwargs.items():
            if hasattr(movie, attribute) and value is not None:
                setattr(movie, attribute, value)
        self.session.add(movie)
        self.session.commit()

class SQLiteMemoryAdapter(SQLAlchemyAdapter):
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

class IMDBCSVAdapter():
    import csv

    def __init__(self, filename):
        self.filename = filename
        self.movies = _read_csv()

    def get_movies(self):
        return movies

    def add(self, title=None, year=None, date_seen=None, imdb=None, comment=None):
        self.movies.append(SeenMovie(title=title, year=year, date_seen=date_seen, imdb=imdb,
                                     comment=comment))

    def get(self, title):
        if movie := [i for i in movies if i.title == title]:
            return movie[0]

    def _read_csv(self):
        with open(self.filename) as csvfile:
            header = csvfile.readline()
            moviereader = csv.reader(csvfile)
            movies = [SeenMovie(title=i[3],
                                year=i[8],
                                date_seen=i[2],
                                imdb=i[0]) for i in moviereader]
        return movies
