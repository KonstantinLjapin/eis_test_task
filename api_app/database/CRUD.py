from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas, models


async def create_houses(db: DatabaseHelper, houses: list[schemas.HouseUpLoad]) -> None:
    async with db.session_factory() as session:
        async with session.begin():
            for house in houses:
                db_house = models.House(address=house.address)
                session.add(db_house)
                await session.flush()
                await session.refresh(db_house)
                fk_house: int = db_house.id
                for apartment in house.apartments:
                    db_apartment = models.Apartment(house_id=fk_house, area=apartment.area,
                                                    water_supply_bill=apartment.water_supply_bill,
                                                    common_property_bill=apartment.common_property_bill)
                    session.add(db_apartment)
                    await session.flush()
                    await session.refresh(db_apartment)
                    fk_apartment = db_apartment.id
                    db_tariff = models.Tariff(apartment_id=fk_apartment,
                                              rate_per_unit_of_water=apartment.tariff.rate_per_unit_of_water,
                                              rate_per_square_meter=apartment.tariff.rate_per_square_meter)
                    session.add(db_tariff)
                    for _ in range(apartment.count_water_meters):
                        db_wm = models.WaterMeter(apartment_id=fk_apartment)
                        session.add(db_wm)
                        await session.flush()
                        await session.refresh(db_wm)
            await session.commit()


async def calculator() -> None:
    db: DatabaseHelper = DatabaseHelper()
    engine: AsyncEngine = db.engine
    async with (db.session_factory() as session):
        for apartment in (await session.scalars(select(models.Apartment))).all():
            tariff: models.Tariff = (await apartment.awaitable_attrs.tariff)[0]
            apartment.common_property_bill = apartment.common_property_bill + (apartment.area
                                                                               * tariff.rate_per_square_meter)
            water_meters_ids: list = [w_m.id for w_m in await apartment.awaitable_attrs.water_meter]
            water_meters_readings_diff: list = []
            for wm_id in water_meters_ids:
                query: select = select(models.Reading).where(models.Reading.water_meter_id == wm_id)
                readings = (await session.scalars(query)).all()
                water_meters_readings_diff.append(readings[-1].value - readings[-2].value)
            apartment.water_supply_bill = apartment.water_supply_bill + (sum(water_meters_readings_diff)
                                                                         * tariff.rate_per_unit_of_water)
            session.add(apartment)
            await session.flush()
            await session.refresh(apartment)
        await session.commit()
    await engine.dispose()


async def get_houses(db: DatabaseHelper, ) -> list[schemas.HouseGet]:
    out: list[schemas.HouseGet] = []
    async with db.session_factory() as session:
        for house in (await session.scalars(select(models.House))).all():
            out_house: schemas.HouseGet = schemas.HouseGet(id=house.id, address=house.address, apartments=[])
            for apart in await house.awaitable_attrs.apartment:
                tariff: models.Tariff = (await apart.awaitable_attrs.tariff)[0]
                out_tariff: schemas.TariffGet = schemas.TariffGet(id=tariff.id, apartment_id=tariff.apartment_id,
                                                                  rate_per_square_meter=tariff.rate_per_square_meter,
                                                                  rate_per_unit_of_water=tariff.rate_per_unit_of_water)
                out_apart: schemas.ApartmentGet = schemas.ApartmentGet(id=apart.id, house_id=out_house.id,
                                                                       water_supply_bill=apart.water_supply_bill,
                                                                       common_property_bill=apart.common_property_bill,
                                                                       area=apart.area, tariff=out_tariff,
                                                                       water_meters=[])
                for water_meter in await apart.awaitable_attrs.water_meter:
                    out_water_meter: schemas.WaterMeter = schemas.WaterMeter(id=water_meter.id,
                                                                             apartment_id=out_apart.id, reading=[])
                    query: select = select(models.Reading).where(models.Reading.water_meter_id == water_meter.id)
                    for reading in (await session.scalars(query)).all():
                        out_reading: schemas.ReadingGet = schemas.ReadingGet(id=reading.id,
                                                                             water_meter_id=out_water_meter.id,
                                                                             value=reading.value, month=reading.month)
                        out_water_meter.readings.append(out_reading)
                    out_apart.water_meters.append(out_water_meter)
                out_house.apartments.append(out_apart)
            out.append(out_house)
    return out


async def enter_readings(db: DatabaseHelper, readings: list[schemas.ReadingUpLoad]) -> None:
    async with db.session_factory() as session:
        async with session.begin():
            for reading in readings:
                db_reading = models.Reading(month=reading.month, value=reading.value,
                                            water_meter_id=reading.water_meter_id,)
                session.add(db_reading)

            await session.commit()

