from fastapi import FastAPI, Response, Request
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

import app.api.hotel.router as hotel

app = FastAPI()

import debugpy
debugpy.listen(('0.0.0.0', 5678))

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(hotel.router)
