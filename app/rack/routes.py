from flask import render_template, flash, redirect, url_for, json, jsonify, request
from flask import Blueprint
from sqlalchemy import func

from app import db
from app.rack.forms import CreateRackForm, EditRackForm
from models import Rack, Unit, Hardware, UnitHardware

rack = Blueprint('rack_bp', __name__, template_folder='templates', static_folder='static')


@rack.route('/', methods=['GET', 'POST'])
@rack.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('rack/index.html', title="Racks dashboard")


@rack.route('/list', methods=['GET', 'POST'])
def list_rack():
    racks = Rack.query.all()
    return render_template('rack/list.html', title='Racks List', racks_list=racks)


@rack.route('/new', methods=['GET', 'POST'])
def new():
    form = CreateRackForm()
    if form.validate_on_submit():
        rack_item = Rack(name=form.name.data)
        # Créer le rack
        db.session.add(rack_item)
        db.session.commit()
        # Créer les unités
        unit_count = form.numberOfUnits.data
        for i in range(unit_count):
            new_unit = Unit(id_rack=rack_item.id, seq=i + 1)
            db.session.add(new_unit)
        db.session.commit()
        flash(f'Rack {rack_item.name} (ID: {rack_item.id}) added!')
        return redirect(url_for('rack_bp.list_rack'))
    return render_template('rack/edit.html', title='New Rack', form=form)


@rack.route('/edit/<int:rack_id>', methods=['GET', 'POST'])
def edit(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    form = EditRackForm(obj=rack_item)
    if form.validate_on_submit():
        if form.submit.data:
            form.populate_obj(rack_item)
            db.session.commit()
            flash(f'Rack {rack_item.name} (id: {rack_item.id}) was updated!')
        return redirect(url_for('rack_bp.list_rack'))
    return render_template('rack/edit.html', title='Edit Rack', form=form)


@rack.route('toggle-activate/<int:rack_id>', methods=('GET', 'POST'))
def toggle_activate(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    rack_item.active = not rack_item.active
    db.session.commit()
    activation_status = "activated" if rack_item.active else "deactivated"
    flash(f'Rack {rack_item.name} (ID: {rack_item.id}) {activation_status}')
    return redirect(url_for('rack_bp.list_rack'))


@rack.route('/delete/<int:rack_id>', methods=['GET', 'POST'])
def delete(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    db.session.delete(rack_item)
    db.session.commit()
    flash(f'Rack {rack_item.name} (ID: {rack_item.id}) deleted!')
    return redirect(url_for('rack_bp.list_rack'))


@rack.route('/view/<int:rack_id>', methods=['GET', 'POST'])
def view(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    return render_template('rack/view.html', title='Units', rack=rack_item)


@rack.route('/api_get_units/<int:rack_id>', methods=['GET', 'POST'])
def get_units(rack_id):
    rack_item = Rack.query.filter_by(id=rack_id, active=True).first_or_404()
    units = [{'id': unit.id, 'name': unit.name, 'seq': unit.seq} for unit in rack_item.units]
    return jsonify({'units': units})


@rack.route('rack_hardware_count/<int:rack_id>', methods=['GET', 'POST'])
def rack_hardware_count(rack_id):
    hardware_count = db.session.query(func.count(Hardware.id)).join(UnitHardware).join(Unit).join(Rack).filter(
        Rack.id == rack_id).scalar()
    return str(hardware_count)


@rack.route('add_unit/<int:rack_id>', methods=['GET', 'POST'])
def add_unit(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    new_unit = Unit(id_rack=rack_item.id, seq=len(rack_item.units) + 1)
    db.session.add(new_unit)
    db.session.commit()
    flash(f'Unit {new_unit.seq} added to rack {rack_item.name} (ID: {rack_item.id})')
    return redirect(url_for('rack_bp.list_rack'))


@rack.route('remove_unit/<int:rack_id>', methods=['GET', 'POST'])
def remove_unit(rack_id):
    rack_item = Rack.query.get_or_404(rack_id)
    units = rack_item.units
    # Vérifier si des matériels sont liés au dernier unit_hardware de la dernière unité du rack
    if units:
        last_unit = units[-1]
        if last_unit.unit_hardware:
            last_unit_hardware = last_unit.unit_hardware[-1]  # Récupérer le dernier unit_hardware de la dernière unité
            if last_unit_hardware.hardware:
                flash(
                    f'Cannot remove unit {last_unit.seq} from rack {rack_item.name} (ID: {rack_item.id}). Hardware is linked to this unit.')
                return redirect(url_for('rack_bp.list_rack'))
        else:
            # Supprimer la dernière unité du rack si aucun matériel n'est lié
            db.session.delete(last_unit)
            db.session.commit()
            flash(f'Unit {last_unit.seq} removed from rack {rack_item.name} (ID: {rack_item.id})')
    else:
        flash(f'No units found to remove from rack {rack_item.name} (ID: {rack_item.id})')

    return redirect(url_for('rack_bp.list_rack'))


@rack.route('edit_unit', methods=['GET', 'POST'])
def edit_unit():
    unit_id = request.form.get('unit_id')
    unit_name = request.form.get('unit_name')
    unit = Unit.query.get_or_404(unit_id)
    unit.name = unit_name
    db.session.commit()
    return json.dumps({'success': True, 'unit_name': unit_name, 'unit_id': unit_id})


@rack.route('unlink_hardware/<int:unit_hardware_id>', methods=['GET', 'POST'])
def unlink_hardware(unit_hardware_id):
    unit_hardware = UnitHardware.query.get_or_404(unit_hardware_id)
    rack_id = unit_hardware.unit.id_rack
    db.session.delete(unit_hardware)
    db.session.commit()
    return redirect(url_for('rack_bp.view', rack_id=rack_id))
