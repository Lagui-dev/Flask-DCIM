from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from app import db
from app.rack.forms import CreateRackForm, EditRackForm
from models import Rack

rack = Blueprint('rack_bp', __name__, template_folder='templates', static_folder='static')

# from app.rack import rack
@rack.route('/', methods=['GET'])
@rack.route('/index', methods=['GET'])
def index():
    return render_template('rack/index.html', title="Racks", activeRack='active')

@rack.route('/list', methods=['GET'])
def list():
    racks = Rack.query.all()
    return render_template('rack/list.html', title='Racks', racks=racks, activeRack='active')

@rack.route('/add', methods=['GET', 'POST'])
def addRack():
    form = CreateRackForm()
    if form.validate_on_submit():
        rack = Rack(name = form.name.data)
        db.session.add(rack)
        db.session.commit()
        flash('Rack added!')
        return redirect(url_for('rack_bp.list'))
    return render_template('rack/edit.html', title='Racks', form=form)

@rack.route('/edit/<int:rack_id>', methods=['GET', 'POST'])
def editRack(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    form = EditRackForm(obj=rack)
    if form.validate_on_submit():
        form.populate_obj(rack)
        db.session.add(rack)
        db.session.commit()
        flash('Rack edited!')
        return redirect(url_for('rack_bp.list'))
    return render_template('rack/edit.html', title='Racks', form=form)

@rack.route('deactivate/<int:rack_id>', methods=('GET', 'POST'))
def deactivateRack(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    rack.active = False
    db.session.commit()
    flash('Rack deactivated')
    return redirect(url_for('rack_bp.list'))

@rack.route('toggle-activate/<int:rack_id>/toggle-active', methods=('GET', 'POST'))
def toggleRackActivate(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    rack.active = not rack.active
    db.session.commit()
    flash('Rack activated/deactivated')
    return redirect(url_for('rack_bp.list'))
