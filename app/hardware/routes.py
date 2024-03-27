from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from app import db
from app.hardware.forms import CreateHardwareForm
from models import Hardware, Unit, UnitHardware

hardware = Blueprint('hardware_bp', __name__, template_folder='templates', static_folder='static')

@hardware.route('/', methods=['GET', 'POST'])
def index():
    return render_template('hardware/index.html', title="Hardware", active_hardware='active')
@hardware.route('/new', methods=['GET', 'POST'])
def new():
    form = CreateHardwareForm()
    if form.validate_on_submit():
        hardware = Hardware(name = form.name.data, type=form.type.data)
        db.session.add(hardware)
        db.session.commit()
        flash('New hardware was created!')
        return redirect(url_for('hardware_bp.index'))
    return render_template('hardware/edit.html', title="New Hardware", form=form, active_hardware='active')

@hardware.route('/list', methods=['GET', 'POST'])
def list():
    pass

@hardware.route('/linked', methods=['GET', 'POST'])
def linked():
    unit_instance = Unit.query.get(1)
    hardware_instance = Hardware.query.get(1)
    unit_hardware_instance = UnitHardware(unit=unit_instance, hardware=hardware_instance)
    db.session.add(unit_hardware_instance)
    db.session.commit()
    return "OK"