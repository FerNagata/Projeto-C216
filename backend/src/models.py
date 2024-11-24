from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os
import datetime

# Modelo para adicionar novas acomodações
class Accommodation(BaseModel):
    category: str
    city: str
    address: str
    idioma: str
    price_per_night: float
    owner: str

class Booking(BaseModel):
    accommodation_id: int
    name: str
    total_price: float
    checkin: datetime
    checkout: datetime
