from flask import render_template
from flask import Blueprint

rack = Blueprint('rack_bp', __name__, template_folder='templates', static_folder='static')

# from app.rack import rack
@rack.route('/', methods=['GET'])
@rack.route('/index', methods=['GET'])
def index():
    print('rack ')
    return render_template('rack/index.html', activeRack='active')
