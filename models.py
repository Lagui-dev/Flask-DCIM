from sqlalchemy import Integer, DateTime, String, ForeignKey, Boolean, UniqueConstraint, Column
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app import db


class TimeMixin(object):
    # Keep track when records are created and updated.
    created = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated = Column(DateTime, nullable=True, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))
    active = Column(Boolean, nullable=True, default=True)


class Rack(TimeMixin, db.Model):
    __tablename__ = 'rack'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    units = relationship('Unit', back_populates='rack')


class Unit(TimeMixin, db.Model):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    seq = Column(Integer, nullable=False)
    id_rack = Column(Integer, ForeignKey('rack.id'))
    name = Column(String(50), nullable=True)

    rack = relationship('Rack', back_populates='units')
    unit_hardware = relationship('UnitHardware', uselist=True, back_populates='unit')
    # interfaces = relationship('Interface', back_populates='unit')


class Hardware(TimeMixin, db.Model):
    __tablename__ = 'hardware'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    hardware_unit = relationship('UnitHardware', uselist=True, back_populates='hardware')
    interfaces = relationship('Interface', back_populates='hardware')


class UnitHardware(TimeMixin, db.Model):
    __tablename__ = 'unit_hardware'

    id = Column(Integer, primary_key=True)
    id_unit = Column(Integer, ForeignKey('unit.id'))
    id_hardware = Column(Integer, ForeignKey('hardware.id'))

    unit = relationship('Unit', back_populates='unit_hardware')
    hardware = relationship('Hardware', back_populates='hardware_unit')
    __table_args__ = (
        UniqueConstraint('id_unit', 'id_hardware', name='unit_hardware_uc'),
    )


class Interface(TimeMixin, db.Model):
    __tablename__ = 'interface'

    id = Column(Integer, primary_key=True)
    id_hardware = Column(Integer, ForeignKey('hardware.id'))
    # id_unit = Column(Integer, ForeignKey('unit.id'))
    name = Column(String(50))
    type = Column(String(50))
    seq = Column(Integer)

    hardware = relationship('Hardware', back_populates='interfaces')
    # unit = relationship('Unit', back_populates='interfaces