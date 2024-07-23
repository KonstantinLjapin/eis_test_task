import uvicorn
import asyncio
from api_app.database.databese import DatabaseHelper, base_create
from api_app.database import schemas, models, CRUD
from fastapi import FastAPI, Depends, HTTPException, Request, Response

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


@app.post("/item", response_model=schemas.ItemBase)
async def get_main(item: schemas.ItemBase, db: DatabaseHelper = Depends(get_db)):
    await CRUD.create_item(db, item)
    return item


@app.get("/items", response_model=list[schemas.ItemBase])
async def get_main(db: DatabaseHelper = Depends(get_db)):
    out: list = await CRUD.get_item(db)
    return out


@app.post("/enter_houses_data", response_model=list[schemas.HouseUpLoad])
async def enter_houses_data(houses: list[schemas.HouseUpLoad], db: DatabaseHelper = Depends(get_db)):
    await CRUD.create_house(db, houses)
    return houses


@app.get("/out_houses_data", response_model=None)
async def out_houses_data(db: DatabaseHelper = Depends(get_db)):
    out: list[schemas.HouseGet] = await CRUD.get_houses(db)
    print(out)
    return


@app.post("/start_calculator", response_model=bool)
async def start_calculator(db: DatabaseHelper = Depends(get_db)):
    pass
    return True

if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
