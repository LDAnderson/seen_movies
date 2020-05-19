from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from seen_movies import SeenMovie, Base

DB_USER = "myapp"
DB_PASS = "dbpass"
DB_HOST = "127.0.0.1"
DB_PORT = 15432
DB_NAME = "movies_seen"

class SQLAlchemyAdapter():
    def __init__(self):
        self.engine = \
        create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_movies(self):
        return self.session.query(SeenMovie).all()

    def add(self, title=None, year=None, date_seen=None, imdb=None, comment=None):
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

class SQLiteMemoryAdapter(SQLAlchemyAdapter):
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
