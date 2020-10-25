from datetime import date

import pytest

import csv
from movies.authentication.services import AuthenticationException
from movies.showcase import services as showcase_services
from movies.authentication import services as auth_services
from movies.showcase.services import NonExistentMovieException
from movies.domain.model import Movie, Genre, Director, Actor, Review, User


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the review.
    showcase_services.add_review(movie_id, review_text, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = showcase_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 7
    review_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(showcase_services.NonExistentMovieException):
        showcase_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(showcase_services.UnknownUserException):
        showcase_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = showcase_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2014
    assert movie_as_dict['title'] == 'Guardians of the Galaxy'
    assert movie_as_dict['description'] == ('A group of intergalactic criminals are forced to work together to stop a '
                                            'fanatical warrior from taking control of the universe.')
    assert len(movie_as_dict['reviews']) == 0
    assert movie_as_dict['actors'] == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"),
                                       Actor("Zoe Saldana")]
    assert movie_as_dict['genres'] == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    assert movie_as_dict['director'] == Director("James Gunn")


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 7

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(showcase_services.NonExistentMovieException):
        showcase_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = showcase_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = showcase_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1000


def test_get_movies_by_date_with_one_date(in_memory_repo):
    target_date = date.fromisoformat('2020-02-28')

    movies_as_dict, prev_date, next_date = showcase_services.get_movies_by_date(target_date, in_memory_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['id'] == 1

    assert prev_date is None
    assert next_date == date.fromisoformat('2020-02-29')


def test_get_movies_by_date_with_multiple_dates(in_memory_repo):
    target_date = date.fromisoformat('2020-03-01')

    movies_as_dict, prev_date, next_date = showcase_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are 3 movies dated 2020-03-01.
    assert len(movies_as_dict) == 3

    # Check that the movie ids for the the movies returned are 3, 4 and 5.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([3, 4, 5]).issubset(movie_ids)

    # Check that the dates of movies surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_date == date.fromisoformat('2020-02-29')
    assert next_date == date.fromisoformat('2020-03-05')


def test_get_movies_by_date_with_non_existent_date(in_memory_repo):
    target_date = date.fromisoformat('2020-03-06')

    movies_as_dict, prev_date, next_date = showcase_services.get_movies_by_date(target_date, in_memory_repo)

    # Check that there are no movies dated 2020-03-06.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [5, 6, 7, 8]
    movies_as_dict = showcase_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the movie ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([5, 6]).issubset(movie_ids)


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = showcase_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 2 reviews were returned for movie with id 1.
    assert len(reviews_as_dict) == 2

    # Check that the reviews relate to the movie whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = showcase_services.get_reviews_for_movie(7, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = showcase_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0
