from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


class House(Base):
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)

    apartment = relationship('Apartment', back_populates='house')


class Apartment(Base):
    __tablename__ = 'apartment'

    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('house.id'), nullable=False)
    area = Column(Float, nullable=False)
    water_supply_bill = Column(Float, nullable=True)
    common_property_bill = Column(Float, nullable=True)
    house = relationship('House', back_populates='apartment')
    water_meter = relationship('WaterMeter', back_populates='apartment')
    tariff = relationship('Tariff', back_populates='apartment')


class WaterMeter(Base):
    __tablename__ = 'water_meter'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'), nullable=False)

    apartment = relationship('Apartment', back_populates='water_meter', lazy='noload')
    reading = relationship('Reading', back_populates='water_meter', lazy='noload')


class Reading(Base):
    __tablename__ = 'reading'

    id = Column(Integer, primary_key=True)
    water_meter_id = Column(Integer, ForeignKey('water_meter.id'), nullable=False)
    month = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    water_meter = relationship('WaterMeter', back_populates='reading', lazy='noload')


class Tariff(Base):
    __tablename__ = 'tariff'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'), nullable=False)
    apartment = relationship('Apartment', back_populates='tariff', lazy='noload')
    rate_per_square_meter = Column(Float, nullable=False)
    rate_per_unit_of_water = Column(Float, nullable=False)

