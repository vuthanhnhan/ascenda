from fastapi import APIRouter, Request, Query
from .repository import HotelRepository
from typing import List

router = APIRouter(
    prefix="/api/hotel",
    tags=["hotel"],
)

hotelRepository = HotelRepository()
@router.get("/", responses={ 200: {} })
async def get_hotel(request: Request, hotel_ids: List[str] = Query([]), destination_id: int = None):
    return await hotelRepository.get_hotels(hotel_ids, destination_id)