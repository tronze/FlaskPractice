from flask import Blueprint, request, render_template, abort, redirect, url_for, session

from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User
from app.database import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.email == username).one_or_none()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.uid
            return redirect(url_for('index'))
        else:
            abort(400)
    return render_template('login.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data

        user = User(
            email=email,
            name=name,
            password=password
        )
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
