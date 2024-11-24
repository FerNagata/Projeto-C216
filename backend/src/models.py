from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os
import datetime

# ----------------- Accommodation -----------------
class AccommodationBase(BaseModel):
    category: str
    city: str
    address: str
    idioma: str
    price_per_night: float
    owner: str
class Accommodation(AccommodationBase):
    id: int
class AccommodationUpdate(BaseModel):
    category: Optional[str]
    city: Optional[str]
    address: Optional[str]
    price_per_night: Optional[float]
    owner: Optional[str]

# ----------------- Booking -----------------
class BookingBase(BaseModel):
    accommodation_id: int
    name: str
    checkin: str  
    checkout: str
class Booking(BookingBase):
    id: int
    total_price: float
class BookingUpdate(BaseModel):
    accommodation_id: Optional[int]
    name: Optional[str]
    total_price: Optional[float]
    checkin: Optional[str]
    checkout: Optional[str]