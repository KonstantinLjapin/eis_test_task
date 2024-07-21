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
    __tablename__ = 'houses'

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)

    apartments = relationship('Apartment', back_populates='house')


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('houses.id'), nullable=False)
    area = Column(Float, nullable=False)
    water_supply_bill = Column(Float, nullable=True)
    common_property_bill = Column(Float, nullable=True)
    house = relationship('House', back_populates='apartments')
    water_meters = relationship('WaterMeter', back_populates='apartment')


class WaterMeter(Base):
    __tablename__ = 'water_meters'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartments.id'), nullable=False)

    apartment = relationship('Apartment', back_populates='water_meters', lazy='noload')
    readings = relationship('Reading', back_populates='water_meter', lazy='noload')


class Reading(Base):
    __tablename__ = 'readings'

    id = Column(Integer, primary_key=True)
    water_meter_id = Column(Integer, ForeignKey('water_meters.id'), nullable=False)
    month = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    water_meter = relationship('WaterMeter', back_populates='readings', lazy='noload')


class Tariff(Base):
    __tablename__ = 'tariffs'

    id = Column(Integer, primary_key=True)
    rate_per_square_meter = Column(Float, nullable=False)
    rate_per_unit_of_water = Column(Float, nullable=False)

