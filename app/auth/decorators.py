import functools

from flask import url_for, redirect, g, abort


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def ownership_required(entity, field):

    def decorator(view):

        @functools.wraps(view)
        def wrapped_view(**kwargs):
            obj = entity.query.filter_by(**kwargs).one_or_none()
            user = g.user
            if obj is None:
                abort(404)
            if user is None:
                return redirect(url_for("auth.login"))
            if getattr(obj, field) != user:
                abort(403)
            return view(**kwargs)
        return wrapped_view
    return decorator
