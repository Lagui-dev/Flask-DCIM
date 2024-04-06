from sqlalchemy import Integer, DateTime, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped
from typing import List, Optional
from datetime import datetime, timezone
from app import db


class TimeMixin(object):
    # Keep track when records are created and updated.
    created: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now(timezone.utc),
                                                        onupdate=datetime.now(timezone.utc))
    deleted: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now(timezone.utc))
    active: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)


class Rack(TimeMixin, db.Model):
    __tablename__ = 'rack'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    units: Mapped[List['Unit']] = relationship('Unit', back_populates='rack')


class Unit(TimeMixin, db.Model):
    __tablename__ = 'unit'

    id: Mapped[int] = mapped_column(primary_key=True)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    id_rack: Mapped[int] = mapped_column(ForeignKey('rack.id'))
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    rack: Mapped[Rack] = relationship('Rack', back_populates='units')
    unit_hardware: Mapped[List['UnitHardware']] = relationship('UnitHardware', uselist=True, back_populates='unit')


class Hardware(TimeMixin, db.Model):
    __tablename__ = 'hardware'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    hardware_unit: Mapped[List['UnitHardware']] = relationship('UnitHardware', uselist=True, back_populates='hardware')


class UnitHardware(TimeMixin, db.Model):
    __tablename__ = 'unit_hardware'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_unit: Mapped[int] = mapped_column(ForeignKey('unit.id'))
    id_hardware: Mapped[int] = mapped_column(ForeignKey('hardware.id'))
    unit: Mapped[Unit] = relationship(back_populates='unit_hardware')
    hardware: Mapped['Hardware'] = relationship(back_populates='hardware_unit')
    __table_args__ = (
        UniqueConstraint('id_unit', 'id_hardware', name='unit_hardware_uc'),
    )
