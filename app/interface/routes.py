from typing import Any

from flask import Blueprint
from flask import render_template, flash, redirect, url_for

from app import db
from app.interface.forms import CreateInterfaceForm, EditInterfaceForm
from models import Interface, Hardware

interface = Blueprint('interface_bp', __name__, template_folder='templates', static_folder='static')


@interface.route('/', methods=['GET', 'POST'])
@interface.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('interface/index.html')


@interface.route('/list', methods=['GET', 'POST'])
def list_interface():
    interface_list: list[Any] = Interface.query.all()
    return render_template('interface/list.html', title='List of Interface', interface_list=interface_list)


@interface.route('/new', methods=['GET', 'POST'])
@interface.route('/new/<int:hardware_id>', methods=['GET', 'POST'])
def new(hardware_id=None):
    form = CreateInterfaceForm()
    if hardware_id:
        hardware = Hardware.query.get_or_404(hardware_id)
        form.hardware.choices = [(hardware.id, hardware.name)]
    else:
        form.hardware.choices = [(hardware.id, hardware.name) for hardware in
                                 Hardware.query.filter_by(active=True).order_by(Hardware.name).all()]

    if form.validate_on_submit():
        hardware_item = Hardware.query.get(form.hardware.data)
        interface_item = Interface(name=form.name.data, type=form.type.data, hardware=hardware_item)
        db.session.add(interface_item)
        db.session.commit()
        flash('Interface created successfully')
        return redirect(url_for('interface_bp.list_interface'))
    return render_template('interface/edit.html', title='New Interface', form=form)


@interface.route('/edit/<int:interface_id>', methods=['GET', 'POST'])
def edit(interface_id):
    interface_item = Interface.query.get_or_404(interface_id)
    form = EditInterfaceForm(obj=interface_item)
    hardware = Hardware.query.get_or_404(interface_item.hardware.id)
    form.hardware.choices = [(hardware.id, hardware.name)]
    if form.validate_on_submit():
        interface_item.name = form.name.data
        interface_item.type = form.type.data
        db.session.commit()
        flash('Interface updated successfully')
        return redirect(url_for('interface_bp.list_interface'))
    return render_template('interface/edit.html', title='Edit Interface', form=form)


@interface.route('/view/<int:interface_id>', methods=['GET', 'POST'])
def view(interface_id):
    interface_item = Interface.query.get_or_404(interface_id)
    return render_template('interface/view.html', title='View Interface', interface=interface_item)


@interface.route('/toggle-activate/<int:interface_id>', methods=['GET', 'POST'])
def toggle_activate(interface_id):
    interface_item = Interface.query.get_or_404(interface_id)
    interface_item.active = not interface_item.active
    db.session.commit()
    activation_status = 'activated' if interface_item.active else 'deactivated'
    flash(f'Interface {interface_item.name} (id: {interface_item.id}) was {activation_status}!')
    return redirect(url_for('interface_bp.list_interface'))
