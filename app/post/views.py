from flask import Blueprint, render_template, abort, request, g, session, redirect, url_for

from app.auth.decorators import login_required
from app.database import db_session
from app.post.forms import PostForm
from app.post.models import Post

bp = Blueprint('post', __name__, url_prefix='/posts', template_folder='templates/post')


@bp.route('/')
@login_required
def list_posts():
    posts = Post.query.all()
    return render_template('list.html', posts=posts)


@bp.route('/<int:uid>')
@login_required
def retrieve_post(uid):
    post = Post.query.filter(Post.uid == uid).one_or_none()
    if post is None:
        abort(404)
    return render_template('detail.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        author = g.user
        content = form.content.data

        post = Post(
            title=title,
            author=author,
            content=content,
        )
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('post.retrieve_post', uid=post.uid))
    return render_template('form.html', form=form)


@bp.route('/<int:uid>/update', methods=('GET', 'POST'))
@login_required
def update_post(uid):
    post = Post.query.get(uid)
    if post is None:
        abort(404)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db_session.commit()
        return redirect(url_for('post.retrieve_post', uid=post.uid))
    return render_template('form.html', form=form)


@bp.route('/<int:uid>/delete', methods=('GET', 'POST'))
@login_required
def delete_post(uid):
    post = Post.query.get(uid)
    if post is None:
        abort(404)
    if request.method == 'POST':
        db_session.delete(post)
        db_session.commit()
        return redirect(url_for('post.list_posts'))
    return render_template('delete.html', post=post)
