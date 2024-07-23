from api_app.database.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, update
from api_app.database.databese import DatabaseHelper
from api_app.database import schemas, models


async def create_item(db: DatabaseHelper, item: schemas.ItemBase) -> None:
    async with db.session_factory() as session:
        async with session.begin():
            session.add(models.Item(title=item.title, description=item.description))
            stmt = select(models.Item)
            await session.execute(stmt)
            await session.commit()


async def get_item(db: DatabaseHelper) -> list:
    out: list = []
    async with db.session_factory() as session:
        async with session.begin():
            stmt = select(models.Item)
            result = await session.execute(stmt)
            for a in result.scalars():
                out.append(schemas.ItemBase(title=a.title, description=a.description))
    return out


async def create_house(db: DatabaseHelper, houses: list[schemas.HouseUpLoad]) -> None:
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


async def get_houses(db: DatabaseHelper, ) -> list[schemas.HouseGet]:
    out: list[schemas.HouseGet] = []
    async with db.session_factory() as session:
        houses = (await session.scalars(select(models.House))).all()
        for house in houses:
            for apart in await house.awaitable_attrs.apartment:
                apart_m: models.Apartment = apart
    return out
