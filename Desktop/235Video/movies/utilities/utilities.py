from flask import Blueprint, url_for

import movies.adapters.repository as repo
import movies.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_actors_and_urls():
    actor_names = services.get_actor_names(repo.repo_instance)
    actor_urls = dict()
    for name in actor_names:
        actor_urls[name] = url_for('showcase_bp.movies_by_actor', actor=name)

    return actor_urls


def get_directors_and_urls():
    director_names = services.get_director_names(repo.repo_instance)
    director_urls = dict()
    for name in director_names:
        director_urls[name] = url_for('showcase_bp.movies_by_director', director=name)

    return director_urls


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for name in genre_names:
        genre_urls[name] = url_for('showcase_bp.movies_by_actor', genre=name)

    return genre_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    return movies


def get_watchlist_url():
    return url_for('watchlist_bp.add_to_watchlist')
