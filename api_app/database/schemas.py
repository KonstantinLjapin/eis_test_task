from pydantic import BaseModel, ConfigDict
from typing import Union, List, Optional
from datetime import date

from api_app.database import models


class ItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Union[str, None] = None


class ReadingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    month: date
    value: float


class Reading(ReadingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    water_meter_id: int


class WaterMeterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    apartment_id: int


class WaterMeter(WaterMeterBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    readings: List[Reading] = []


class ApartmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    house_id: int
    area: float
    water_supply_bill: Optional[float] = None
    common_property_bill: Optional[float] = None


class Apartment(ApartmentBase):
    model_config = ConfigDict(from_attributes=True)
    water_meters: List[WaterMeter] = []


class ApartmentGet(ApartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    water_meters: List[WaterMeter]


class HouseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    address: str


class House(HouseBase):
    model_config = ConfigDict(from_attributes=True)
    apartments: List[Apartment]


class HouseGet(HouseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    apartments: List[ApartmentGet]


class TariffBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    rate_per_square_meter: float
    rate_per_unit_of_water: float


class Tariff(TariffBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
