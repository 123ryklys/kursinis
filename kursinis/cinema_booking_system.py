from abc import ABC, abstractmethod

class Movie:
    def __init__(self, title, duration, rating):
        self.title = title
        self.duration = duration  # in minutes
        self.rating = rating

    def __str__(self):
        return f"{self.title} - Duration: {self.duration} mins, Rating: {self.rating}"

class Show(ABC):
    def __init__(self, movie, time, screen):
        self.movie = movie
        self.time = time
        self.screen = screen
        self.seats = [[False for _ in range(5)] for _ in range(5)]  

    @abstractmethod
    def display_seats(self):
        pass

    @abstractmethod
    def book_seat(self, row, col):
        pass

    @abstractmethod
    def choose_seats(self, num_seats):
        pass

class MovieShow(Show):
    def display_seats(self):
        print("Seats Layout (True = Booked, False = Available):")
        for row in self.seats:
            print(row)

    def book_seat(self, row, col):
        if self.seats[row][col]:
            print(f"Seat ({row}, {col}) is already booked.")
            return False
        self.seats[row][col] = True
        print(f"Seat ({row}, {col}) booked successfully.")
        return True

    def choose_seats(self, num_seats):
        booked_seats = []
        for _ in range(num_seats):
            while True:
                self.display_seats()
                try:
                    row = int(input("Enter the row number (0-4): "))
                    col = int(input("Enter the column number (0-4): "))
                    if 0 <= row < 5 and 0 <= col < 5:
                        if self.book_seat(row, col):
                            booked_seats.append((row, col))
                            break
                    else:
                        print("Invalid seat. Enter row and column numbers between 0 and 4.")
                except ValueError:
                    print("Invalid input. Enter valid numbers.")
        return booked_seats

class ShowFactory:
    @staticmethod
    def create_show(show_type, movie, time, screen):
        if show_type == "MovieShow":
            return MovieShow(movie, time, screen)
        else:
            raise ValueError(f"Unknown show type: {show_type}")

class Theater:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Theater, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  
            self.movies = []
            self.showtimes = []
            self.initialized = True

    def add_movie(self, movie):
        self.movies.append(movie)

    def list_movies(self):
        print("Movies:")
        for idx, movie in enumerate(self.movies, start=1):
            print(f"{idx}. {movie}")

    def load_movies_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        title, duration, rating = line.split(',')
                        movie = Movie(title.strip(), int(duration.strip()), rating.strip())
                        self.add_movie(movie)
                    except ValueError as ve:
                        print(f"Skipping line due to format error: '{line}'. Error: {ve}")
            
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_showtime(self, showtime):
        self.showtimes.append(showtime)
        

    def list_showtimes(self):
        print("Showtimes:")
        for idx, showtime in enumerate(self.showtimes, start=1):
            print(f"{idx}. {showtime.movie.title} at {showtime.time} on screen {showtime.screen}")

    def load_showtimes_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        movie_title, time, screen = line.split(',')
                        movie = self.find_movie_by_title(movie_title.strip())
                        if movie:
                            showtime = ShowFactory.create_show("MovieShow", movie, time.strip(), int(screen.strip()))
                            self.add_showtime(showtime)
                        else:
                            print(f"Movie '{movie_title.strip()}' not found in the movie list.")
                    except ValueError as ve:
                        print(f"Skipping line due to format error: '{line}'. Error: {ve}")
            
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def find_movie_by_title(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def choose_movie(self):
        if not self.movies:
            print("No movies available.")
            return None
        
        self.list_movies()
        
        while True:
            try:
                choice = int(input("Choose a movie by entering the corresponding number: "))
                if 1 <= choice <= len(self.movies):
                    return self.movies[choice - 1]
                else:
                    print("Invalid choice. Please enter a number within the list range.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def choose_showtime(self):
        if not self.showtimes:
            print("No showtimes available.")
            return None

        self.list_showtimes()

        while True:
            try:
                choice = int(input("Choose a showtime by entering the corresponding number: "))
                if 1 <= choice <= len(self.showtimes):
                    return self.showtimes[choice - 1]
                else:
                    print("Invalid choice. Please enter a number within the list range.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

def print_tickets_to_file(movie, time, duration, seats):
    for seat in seats:
        with open(f'ticket_{movie.title}_seat_{seat[0]}_{seat[1]}.txt', 'w') as file:
            file.write(f"Movie: {movie.title}\n")
            file.write(f"Time: {time}\n")
            file.write(f"Duration: {duration} mins\n")
            file.write(f"Seat: Row {seat[0] + 1}, Column {seat[1] + 1}\n")
            print(f"Ticket for seat {seat} printed.")


theater = Theater()
    
theater.load_movies_from_file('movies.txt')
    
theater.load_showtimes_from_file('showtimes.txt')
    
selected_showtime = theater.choose_showtime()
if selected_showtime:
    print(f"You have selected the showtime for: {selected_showtime.movie}")
    while True:
        try:
            num_seats = int(input("How many seats would you like to book? "))
            if 1 <= num_seats <= 25:
                break
            else:
                print("Invalid number of seats. Please enter a number between 1 and 25.")
        except ValueError:
             print("Invalid input. Please enter a valid number.")
    selected_seats = selected_showtime.choose_seats(num_seats)
    if selected_seats:
         print(f"You have selected seats: {selected_seats}")
         print_tickets_to_file(selected_showtime.movie, selected_showtime.time, selected_showtime.movie.duration, selected_seats)

