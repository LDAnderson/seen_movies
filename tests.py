import unittest
import subprocess

from random import randint


from seen_movies import SeenMovie
from adapter import RemoteServerMovieClient, LocalMovieClient

unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


class TestName(unittest.TestCase):
    def setUp(self):
        self.client = LocalMovieClient()
        self.client.add(title="Test Movie", year=2020, imdb='0123456789', comment="Comment")


    def test_client_postgres(self):
        client = RemoteServerMovieClient()
        movies = client.get_all()

    def test_client(self):
        c = LocalMovieClient()
        self.assertTrue(c.session.is_active)

    def test_client_get(self):
        movie = self.client.get("Test Movie")
        self.assertEqual(movie.title, "Test Movie")
        movie_doesnt_exist = self.client.get("This movie does not exist")
        self.assertEqual(movie_doesnt_exist, None)

    def test_client_add(self):
        self.client.add(title="Gone With the Wind", year=1939, imdb='0031381', comment='Watched this movie tonight.')
        movies = self.client.get_all()
        self.assertIn(("Gone With the Wind", 1939), [(t.title, t.year) for t in movies])

    def test_client_update(self):
        movie = self.client.get("Test Movie")
        self.assertEqual(movie.comment, 'Comment')
        self.client.update(movie, year=2021, comment="New Comment")
        self.assertEqual(movie.year, 2021)
        self.assertEqual(movie.comment, 'New Comment')
        with self.assertRaises(AttributeError):
            self.client.update(movie, good=False)
            self.assertFalse(movie.good)
        self.client.update(movie, comment="")
        self.assertEqual(movie.comment, "")

class SeenMovieTests(unittest.TestCase):
    def setUp(self):
        self.m1 = SeenMovie(title="Scarface", year=1932, imdb='0023427',
                       comment="Grapefruit right to the kisser")

    def test_slug(self):
        t1 = SeenMovie(title="A Long Title!", year=1932)
        self.assertEqual(t1.title,"A Long Title!")
        self.assertEqual(t1.title_slug(), "alongtitle")

        t2 = SeenMovie(title="!!! !", year=2050)
        self.assertNotEqual(t2.title_slug(), "")

    def test_seenmovie(self):
        t1 = SeenMovie(title="Scarface", year=1932, imdb='0023427',
                       comment="Grapefruit right to the kisser")
        self.assertEqual(t1.year, 1932)
        self.assertEqual(self.m1.title, "Scarface")

if __name__.__contains__("__main__"):
    unittest.main(exit=False)
