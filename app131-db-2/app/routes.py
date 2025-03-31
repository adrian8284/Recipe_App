from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash # Added url_for for easier redirect, added flash for UI message feedback
from flask_login import login_user, current_user, logout_user, login_required # Added for login authentication
from app.forms import LoginForm, RecipeForm
from app.models import User, Recipe
from app import db
from werkzeug.security import check_password_hash # Added for added security verification

# Home Page (public)
@myapp_obj.route("/")
@myapp_obj.route("/recipes")
def home():
    recipes = Recipe.query.all()
    return render_template("index.html", recipes=recipes)

# New Recipe Page (requires login)
@myapp_obj.route("/recipe/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!")
        return redirect(url_for("home"))
    return render_template("new_recipe.html", form=form)

# Recipe Detail Page (public)
@myapp_obj.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)

# Delete Recipe Page (requires login and authorization)
@myapp_obj.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        flash("You do not have permission to delete this recipe.")
        return redirect(url_for("home"))
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted successfully!")
    return redirect(url_for("home"))

# Login Page
@myapp_obj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html", form=form)

# Logout Page
@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))