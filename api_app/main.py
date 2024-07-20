import uvicorn
import asyncio
from api_app.database.CRUD import base_create
from fastapi import FastAPI
app = FastAPI()


@app.get("/main", response_model=None)
async def get_main():
    return "out"


if __name__ == "__main__":
    # создаются таблицы в бд
    asyncio.run(base_create())
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
