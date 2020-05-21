
from adapter import SQLAlchemyAdapter, SQLiteMemoryAdapter

class SeenMovieClient():
    adapters = {
        'SQLAlchemy': SQLAlchemyAdapter,
        'SQLite': SQLiteMemoryAdapter,
    }

    def __init__(self, adapter_name):

        self.adapter = SeenMovieClient.adapters[adapter_name]()

    def seen(self):
        return self.adapter.get_movies()


    def add(self, **kwargs):
        return self.adapter.add(**kwargs)

    def get(self, title):
        return self.adapter.get(title)

    def update(self, movie, **kwargs):
        return self.adapter.update(movie, **kwargs)
