from flask import Blueprint, request, render_template, abort, redirect, url_for, session

from app.auth.models import User
from app.database import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.email == username).one_or_none()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.uid
            return redirect(url_for('index'))
        else:
            abort(400)
    return render_template('login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if not email or not password or not name:
            abort(400)

        user = User(
            email=email,
            name=name,
            password=password
        )
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
