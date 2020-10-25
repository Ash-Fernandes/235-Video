from typing import Iterable

from movies.adapters.repository import AbstractRepository
from movies.domain.model import make_review, Movie, Review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    review = make_review(review_text, user, movie)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_watchlist(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user.watchlist


def get_movies_by_ranking(id, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches), the date of the previous movie (might be null),
    # the date of the next movie (might be null)
    list_of_ids = [id]
    movies = repo.get_movies_by_id(list_of_ids)

    movies_dto = list()
    prev_id = next_id = None

    if len(movies) > 0:
        prev_id = repo.get_id_of_previous_movie(movies[0])
        next_id = repo.get_id_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_id, next_id


def get_movie_ids_for_actor(actor_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_actor(actor_name)

    return movie_ids


def get_movie_ids_for_director(director_name, repo: AbstractRepository):
    director_ids = repo.get_movie_ids_for_director(director_name)

    return director_ids


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    genre_ids = repo.get_movie_ids_for_genre(genre_name)

    return genre_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'release_year': movie.release_year,
        'title': movie.title,
        'description': movie.description,
        'actors': movie.actors,
        'director': movie.director,
        'genres': movie.genres,
        'reviews': reviews_to_dict(movie.reviews),
        'hyperlink': movie.hyperlink,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.release_year)
    # Note there's no comments or tags.
    return movie
