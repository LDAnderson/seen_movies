"""
seenmovies.py: Keep track of movies watched in a SQL database
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, \
    MetaData, Table, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
DB_USER = "myapp"
DB_PASS = "dbpass"
DB_HOST = "127.0.0.1"
DB_PORT = 15432
DB_NAME = "movies_seen"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


with engine.connect() as connection:
    print(connection)
    # result = connection.execute("select * from seen")
    # for row in result:
    #     print(row)

Base = declarative_base()

class SeenMovie(Base):
    __tablename__ = 'seenmovies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(200),nullable=False)
    year = Column(Integer())
    date_seen = Column(Date(), default=datetime.now)
    imdb = Column(String(20))
    comment = Column(Text())

    def __repr__(self):
        return f"{self.name} ({self.year}) seen: {self.date_seen}"


m = SeenMovie(name = "Hot Boyz", year=1999, imdb='tt0191191')

from sqlalchemy.orm import sessionmaker, Session
Session = sessionmaker(bind=engine)
session = Session()
