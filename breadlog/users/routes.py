from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from breadlog.users.forms import RegisterForm, LoginForm
from breadlog.models import User
from breadlog.extensions import bcrypt, db

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/recipes') 
    form = RegisterForm()
    if request.method == 'POST' and not form.validate():
        errors = []
        for field, error in form.errors.items():
            for err in error:
                errors.append([field, err])
        return ' '.join([str(i) for i in errors])
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(form.name.data, form.email.data, hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users.login'))
        except:
            return 'There was an error creating user'
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/recipes')  # TODO: replace with something that makes sense 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and the password matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('recipes.get_recipes'))
        else:
            return 'Login unsuccessful'  # TODO: change to a flash message
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect('/')
