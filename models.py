from sqlalchemy import Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import mapped_column, Mapped
from typing import List
from datetime import datetime, timezone
from app import db

class TimeMixin(object):
    # Keep track when records are created and updated.
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class Rack(TimeMixin, db.Model):
    __tablename__ = 'rack'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    units: Mapped[List['Unit']] = relationship('Unit', back_populates='rack')

class Unit(db.Model):
    __tablename__ = 'unit'

    id: Mapped[int] = mapped_column(primary_key=True)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    id_rack:Mapped[int] = mapped_column(ForeignKey('rack.id'))
    name: Mapped[str] = mapped_column(String(50))
    rack: Mapped[Rack] = relationship('Rack', back_populates='units')
