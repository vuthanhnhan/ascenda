from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.hotel.repository import HotelRepository

load_dotenv()

import app.api.hotel.router as hotel

app = FastAPI()

@app.on_event("startup")
async def startup():
    await HotelRepository().init_fetch_all_hotels()

import debugpy
debugpy.listen(('0.0.0.0', 5678))

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(hotel.router)
