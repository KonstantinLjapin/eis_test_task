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
    await CRUD.create_user_item(db, item)
    return item


if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
