from datetime import date

from movies.domain.model import Movie, Genre, Director, Actor, Review, make_review, User

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "Guardians of the Galaxy",
        2014
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def actor():
    return Actor('Chris Pratt')


@pytest.fixture()
def genre():
    return Genre('Action')


@pytest.fixture()
def director():
    return Director('James Gunn')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for review in user.reviews:
        # User should have an empty list of reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.release_year == 2014
    assert movie.title == 'Guardians of the Galaxy'

    assert len(movie.reviews) == 0
    assert len(movie.actors) == 0
    assert len(movie.genres) == 0
    assert movie.director is None

    assert repr(movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_movie_less_than_operator(movie):
    movie1 = Movie(
        "Apples",
        None
    )

    movie2 = Movie(
        'Guardians of the Galaxy',
        2020
    )

    assert movie1 < movie
    assert movie < movie2


def test_actor_construction(actor):
    assert actor.actor_full_name == 'Chris Pratt'

    for colleague in actor.colleagues:
        assert False
