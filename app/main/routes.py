from flask import render_template
from flask import Blueprint

main = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')

@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html', activeMain='active')
