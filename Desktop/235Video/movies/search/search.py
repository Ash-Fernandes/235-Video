from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash
from wtforms import Form, StringField, SelectField

import movies.adapters.repository as repo
import movies.search.services as services

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search = MovieSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search.data['search'], search.data['select'])

    return render_template('search.html',
                           form=search,
                           title="Search database",
                           description="Enter your search below:")


@search_blueprint.route('/results')
def search_results(search, select):
    search = search.title()
    b_exists = services.search_exists(search, select, repo.repo_instance)
    if b_exists:
        if select == "Actor":
            return redirect(url_for('showcase_bp.movies_by_actor', actor=search))
        elif select == "Genre":
            return redirect(url_for('showcase_bp.movies_by_actor', genre=search))
        elif select == "Director":
            return redirect(url_for('showcase_bp.movies_by_director', director=search))
    else:
        flash('Sorry, result not found!')
        return redirect(url_for('search_bp.search'))


class MovieSearchForm(Form):
    choices = [('Actor', 'Actor'),
               ('Director', 'Director'),
               ('Genre', 'Genre')]
    select = SelectField('Search by actor, director, or genre:', choices=choices)
    search = StringField('')
