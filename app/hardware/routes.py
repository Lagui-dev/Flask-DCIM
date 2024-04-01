from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from app import db
from app.hardware.forms import CreateHardwareForm, EditHardwareForm
from models import Hardware, Unit, UnitHardware

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


@hardware.route('/linked', methods=['GET', 'POST'])
def linked():
    unit_instance = Unit.query.get(12)
    hardware_instance = Hardware.query.get(3)
    unit_hardware_instance = UnitHardware(unit=unit_instance, hardware=hardware_instance)
    db.session.add(unit_hardware_instance)
    db.session.commit()
    return "OK"

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



