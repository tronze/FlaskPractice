from flask import Blueprint, render_template, abort, request, g, session, redirect, url_for

from app.auth.models import User
from app.database import db_session
from app.post.models import Post

bp = Blueprint('post', __name__, url_prefix='/posts', template_folder='templates/post')


@bp.route('/')
def list_posts():
    posts = Post.query.all()
    return render_template('list.html', posts=posts)


@bp.route('/<int:uid>')
def retrieve_post(uid):
    post = Post.query.filter(Post.uid == uid).one_or_none()
    if post is None:
        abort(404)
    return render_template('detail.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        author = User.query.get(session.get("user_id"))
        content = request.form.get('content')

        if not title or not content:
            abort(400)
        post = Post(
            title=title,
            author=author,
            content=content,
        )
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('post.retrieve_post', uid=post.uid))
    return render_template('form.html')


@bp.route('/<int:uid>/update', methods=('GET', 'POST'))
def update_post(uid):
    post = Post.query.get(uid)
    if post is None:
        abort(404)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            abort(400)
        post.title = title
        post.content = content
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('post.retrieve_post', uid=post.uid))
    return render_template('form.html', post=post)


@bp.route('/<int:uid>/delete', methods=('GET', 'POST'))
def delete_post(uid):
    post = Post.query.get(uid)
    if post is None:
        abort(404)
    if request.method == 'POST':
        db_session.delete(post)
        db_session.commit()
        return redirect(url_for('post.list_posts'))
    return render_template('delete.html', post=post)
