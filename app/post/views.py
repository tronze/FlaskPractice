from flask import Blueprint

bp = Blueprint('post', __name__, url_prefix='/posts', template_folder='templates/post')