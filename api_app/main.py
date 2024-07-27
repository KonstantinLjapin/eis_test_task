import uvicorn
import asyncio
from api_app.database.databese import DatabaseHelper, base_create
from api_app.database import schemas, models, CRUD
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from celery import Celery, shared_task
import asyncio

celery = Celery(
    'api_app.main',
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@shared_task
def corr_calculate() -> None:
    asyncio.run(CRUD.calculator())


app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = DatabaseHelper()
        response = await call_next(request)
    finally:
        await request.state.db.engine.dispose()
    return response


def get_db(request: Request):
    return request.state.db


@app.post("/enter_houses_data", response_model=list[schemas.HouseUpLoad])
async def enter_houses_data(houses: list[schemas.HouseUpLoad], db: DatabaseHelper = Depends(get_db)):
    try:
        await CRUD.create_houses(db, houses)
        return Response("Ok", status_code=200)
    except Exception as e:
        return Response(f"{e}", status_code=500)


@app.get("/out_houses_data", response_model=list[schemas.HouseGet])
async def out_houses_data(db: DatabaseHelper = Depends(get_db)):
    try:
        out: list[schemas.HouseGet] = await CRUD.get_houses(db)
        return out
    except Exception as e:
        return Response(f"{e}", status_code=500)


@app.post("/enter_readings_data", response_model=list[schemas.ReadingUpLoad])
async def enter_houses_data(readings: list[schemas.ReadingUpLoad], db: DatabaseHelper = Depends(get_db)):
    try:
        await CRUD.enter_readings(db, readings)
        return Response("Ok", status_code=200)
    except Exception as e:
        return Response(f"{e}", status_code=500)


@app.post("/start_calculator", response_model=bool)
async def start_calculator():
    try:
        corr_calculate.delay()
        return Response("Ok", status_code=200)
    except Exception as e:
        return Response(f"{e}", status_code=500)


if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
