from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from app import db
from app.rack.forms import CreateRackForm, EditRackForm
from models import Rack, Unit

rack = Blueprint('rack_bp', __name__, template_folder='templates', static_folder='static')

@rack.route('/', methods=['GET', 'POST'])
@rack.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('rack/index.html', title="Racks")

@rack.route('/list', methods=['GET', 'POST'])
def list():
    racks = Rack.query.all()
    return render_template('rack/list.html', title='Racks', racks=racks)

@rack.route('/new', methods=['GET', 'POST'])
def new():
    form = CreateRackForm()
    if form.validate_on_submit():
        rack = Rack(name = form.name.data)
        # Créer le rack
        db.session.add(rack)
        db.session.commit()
        # Créer les unités
        unitCount = form.numberOfUnits.data
        for i in range(unitCount):
            new_unit = Unit(id_rack=rack.id, seq=i + 1)
            db.session.add(new_unit)
        db.session.commit()
        flash(f'Rack {rack.name} (ID: {rack.id}) added!')
        return redirect(url_for('rack_bp.list'))
    return render_template('rack/edit.html', title='New Rack', form=form)

@rack.route('/edit/<int:rack_id>', methods=['GET', 'POST'])
def edit(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    form = EditRackForm(obj=rack)
    if form.validate_on_submit():
        if form.submit.data:
            form.populate_obj(rack)
            db.session.add(rack)
            db.session.commit()
            flash(f'Rack {rack.name} (ID: {rack.id}) edited!')
            return redirect(url_for('rack_bp.list'))
        else:
            return redirect(url_for('rack_bp.list'))
    return render_template('rack/edit.html', title='Edit Rack', form=form)

@rack.route('toggle-activate/<int:rack_id>/toggle-active', methods=('GET', 'POST'))
def toggle_activate(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    rack.active = not rack.active
    db.session.commit()
    activation_status = "activated" if rack.active else "deactivated"
    flash(f'Rack {rack.name} (ID: {rack.id}) {activation_status}')
    return redirect(url_for('rack_bp.list'))

@rack.route('/delete/<int:rack_id>', methods=['GET', 'POST'])
def delete(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    db.session.delete(rack)
    db.session.commit()
    flash(f'Rack {rack.name} (ID: {rack.id}) deleted!')
    return redirect(url_for('rack_bp.list'))

@rack.route('/view/<int:rack_id>', methods=['GET', 'POST'])
def view(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    return render_template('rack/view.html', title='Rack', rack=rack)