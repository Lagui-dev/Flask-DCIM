from flask import render_template, flash, redirect, url_for, request
from flask import Blueprint


from app import db
from app.hardware.forms import CreateHardwareForm, EditHardwareForm, LinkHardwareUnitForm
from models import Hardware, Unit, UnitHardware, Rack

hardware = Blueprint('hardware_bp', __name__, template_folder='templates', static_folder='static')

@hardware.route('/', methods=['GET', 'POST'])
def index():
    return render_template('hardware/index.html', title="Hardware dashboard", active_hardware='active')
@hardware.route('/new', methods=['GET', 'POST'])
def new():
    form = CreateHardwareForm()
    if form.validate_on_submit():
        hardware = Hardware(name = form.name.data, type=form.type.data)
        db.session.add(hardware)
        db.session.commit()
        flash('New hardware was created!')
        return redirect(url_for('hardware_bp.index'))
    return render_template('hardware/edit.html', title="New Hardware", form=form)

@hardware.route('/list', methods=['GET', 'POST'])
def list():
    hardware_list = Hardware.query.all()
    return render_template('hardware/list.html', title="Hardware List", hardware_list=hardware_list)

@hardware.route('/view/<int:hardware_id>', methods=['GET', 'POST'])
def view(hardware_id):
    pass

@hardware.route('/edit/<int:hardware_id>', methods=['GET', 'POST'])
def edit(hardware_id):
    hardware = Hardware.query.get(hardware_id)
    form = EditHardwareForm(obj=hardware)
    if form.validate_on_submit():
        if form.submit.data:
            form.populate_obj(hardware)
            db.session.commit()
            flash(f'Hardware {hardware.name} (id: {hardware.id}) was updated!')
        return redirect(url_for('hardware_bp.list'))
    return render_template('hardware/edit.html', title="Edit Hardware", form=form)
    pass

@hardware.route('/toggle-activate/<int:hardware_id>', methods=['GET', 'POST'])
def toggle_activate(hardware_id):
    pass

@hardware.route ('/link_hardware_unit/<int:hardware_id>', methods=['GET', 'POST'])
def link_hardware_unit(hardware_id):
    form = LinkHardwareUnitForm()
    form.rack.choices = [(rack.id, rack.name) for rack in Rack.query.filter_by(active=True).all()]

    if form.rack.choices:
        first_rack_id = form.data['rack']
        print(first_rack_id)
        if first_rack_id is None:
            first_rack_id = form.rack.choices[0][0]
        units_of_rack = Unit.query.filter(Unit.id_rack == first_rack_id).all()
        form.unit.choices = [(unit.id, f"{unit.seq} - {unit.name}" if unit.name is not None else str(unit.seq)) for unit in units_of_rack]
    else:
        flash('No rack found!')
        return redirect(url_for('hardware_bp.list'))
    id_unit = form.unit.data
    hardware = Hardware.query.get(hardware_id)
    if form.validate_on_submit():
        unit = Unit.query.get(id_unit)
        # vérifier si le lien existe déjà
        existing_link = UnitHardware.query.filter_by(id_unit=id_unit, id_hardware=hardware_id).first()
        if existing_link:
            # ICI
            flash('This link already exists!')
        else:
            print(form.data)
            new_link = UnitHardware(unit=unit, hardware=hardware)
            db.session.add(new_link)
            db.session.commit()
            flash('Hardware was linked to unit!')
            return redirect(url_for('hardware_bp.list'))
    return render_template('hardware/link_hardware_unit.html', title="Link Hardware to Unit",
                           form=form, hardware=hardware)