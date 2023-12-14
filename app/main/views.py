from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.main import main
from app.main.forms import RecipeForm, SearchForm
from app.model import Recipe, User


@main.route('/', methods=['GET', 'POST'])
def index():
    # recipes from database
    recipes = Recipe.query.order_by(Recipe.created)
    return render_template('index.html', recipes=recipes)


# Uploading a recipe
@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data,
                        ingredients=form.ingredients.data,
                        method=form.method.data,
                        public=form.public.data,
                        meal=form.meal.data,
                        author_id=current_user.username,
                        )
        db.session.add(recipe)
        db.session.commit()
        flash('Successfully uploaded recipe.')
        return redirect(url_for('main.index'))
    return render_template('/create.html', form=form)


# Recipe view
@main.route('/recipe/<int:id>')
def recipe(id):
    # Query recipe for matching id
    recipe = Recipe.query.get_or_404(id)
    # publish if owner or public
    if recipe.public \
            or (not recipe.public
                and current_user.is_authenticated
                and recipe.author_id == current_user.username):
        return render_template('recipe.html', recipe=recipe)
    flash('This recipe is private')
    return redirect(url_for('main.index'))


# Updating an existing recipe
@main.route('/recipe/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author_id != current_user.username:
        flash('You cannot edit as you are not the author')
        return redirect(url_for('main.index'))
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.method = form.method.data
        recipe.ingredients = form.ingredients.data
        recipe.meal = form.meal.data
        recipe.public = form.public.data
        db.session.add(recipe)
        db.session.commit()
        flash('The recipe has been updated.')
        return redirect(url_for('main.recipe', id=recipe.id))
    form.title.data = recipe.title
    form.method.data = recipe.method
    form.ingredients.data = recipe.ingredients
    form.meal.data = recipe.meal
    form.public.data = recipe.public
    return render_template('/update.html', form=form, recipe=recipe)


@main.route('/recipe/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    Recipe.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))


# Pass function to navbar, required for search form to use CSRF token
@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Search function
@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipe.query
    users = User.query
    if form.validate_on_submit():
        # Get data from submitted form
        searched = form.searched.data
        # Query the database
        recipes = recipes.filter(Recipe.title.like('%' + searched + '%'))
        recipes = recipes.order_by(Recipe.title).all()
        users = users.filter(User.username.like('%' + searched + '%'))
        users = users.order_by(User.username).all()
        return render_template("search.html",
                               form=form,
                               searched=searched,
                               recipes=recipes,
                               users=users)


# Unimplemented features PLEASE IGNORE
# File submit
"""

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    pass

"""
