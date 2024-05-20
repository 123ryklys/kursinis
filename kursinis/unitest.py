import unittest
from unittest.mock import patch, mock_open
from io import StringIO

# Importing the necessary classes from the theater module
from theater import Movie, MovieShow, ShowFactory, Theater, print_tickets_to_file

class TestMovie(unittest.TestCase):
    def test_movie_initialization(self):
        movie = Movie("Inception", 148, "PG-13")
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.duration, 148)
        self.assertEqual(movie.rating, "PG-13")
    
    def test_movie_str(self):
        movie = Movie("Inception", 148, "PG-13")
        self.assertEqual(str(movie), "Inception - Duration: 148 mins, Rating: PG-13")

class TestMovieShow(unittest.TestCase):
    def setUp(self):
        self.movie = Movie("Inception", 148, "PG-13")
        self.movie_show = MovieShow(self.movie, "18:00", 1)
    
    def test_initial_seats(self):
        for row in self.movie_show.seats:
            self.assertEqual(row, [False] * 5)
    
    def test_book_seat_success(self):
        result = self.movie_show.book_seat(2, 3)
        self.assertTrue(result)
        self.assertTrue(self.movie_show.seats[2][3])
    
    def test_book_seat_failure(self):
        self.movie_show.seats[2][3] = True
        result = self.movie_show.book_seat(2, 3)
        self.assertFalse(result)
        self.assertTrue(self.movie_show.seats[2][3])

class TestShowFactory(unittest.TestCase):
    def test_create_movie_show(self):
        movie = Movie("Inception", 148, "PG-13")
        show = ShowFactory.create_show("MovieShow", movie, "18:00", 1)
        self.assertIsInstance(show, MovieShow)
    
    def test_create_unknown_show(self):
        movie = Movie("Inception", 148, "PG-13")
        with self.assertRaises(ValueError):
            ShowFactory.create_show("UnknownShow", movie, "18:00", 1)

class TestTheater(unittest.TestCase):
    def setUp(self):
        self.theater = Theater()
        self.movie = Movie("Inception", 148, "PG-13")
    
    def test_singleton_pattern(self):
        theater2 = Theater()
        self.assertIs(self.theater, theater2)
    
    def test_add_and_list_movies(self):
        self.theater.add_movie(self.movie)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.theater.list_movies()
            self.assertIn("1. Inception - Duration: 148 mins, Rating: PG-13", fake_out.getvalue())
    
    @patch("builtins.open", new_callable=mock_open, read_data="Inception,148,PG-13\n")
    def test_load_movies_from_file(self, mock_file):
        self.theater.load_movies_from_file('movies.txt')
        self.assertEqual(len(self.theater.movies), 1)
        self.assertEqual(self.theater.movies[0].title, "Inception")
    
    @patch("builtins.open", new_callable=mock_open, read_data="Inception,18:00,1\n")
    def test_load_showtimes_from_file(self, mock_file):
        self.theater.add_movie(self.movie)
        self.theater.load_showtimes_from_file('showtimes.txt')
        self.assertEqual(len(self.theater.showtimes), 1)
        self.assertEqual(self.theater.showtimes[0].movie.title, "Inception")

class TestUtilityFunctions(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_print_tickets_to_file(self, mock_file):
        movie = Movie("Inception", 148, "PG-13")
        seats = [(0, 0), (1, 1)]
        print_tickets_to_file(movie, "18:00", 148, seats)
        mock_file().write.assert_any_call("Movie: Inception\n")
        mock_file().write.assert_any_call("Time: 18:00\n")
        mock_file().write.assert_any_call("Duration: 148 mins\n")
        mock_file().write.assert_any_call("Seat: Row 1, Column 1\n")

if __name__ == "__main__":
    unittest.main()

