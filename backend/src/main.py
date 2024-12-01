from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import time
from models import AccommodationBase, Accommodation, AccommodationUpdate, BookingBase, Booking, BookingUpdate
from typing import List
import os, asyncpg
import pytz

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/houseReservation") 
    return await asyncpg.connect(DATABASE_URL)

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Middleware for logging
@api.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response
    
# ----------------- Accommodation -----------------

# 1. Adding a new accommodation
@api.post("/api/v1/accommodations", status_code=201)
async def add_accommodation(accommodation: AccommodationBase):
    conn = await get_database()
    # Verify if the accommodation already exists
    # if await get_all_accommodation(accommodation.category, accommodation.city, accommodation.address, conn):
    #     raise HTTPException(status_code=400, detail="A acomodação já existe.")
    try:
        query = """
            INSERT INTO accommodation (category, city, address, price_per_night, owner)
            VALUES ($1, $2, $3, $4, $5)
        """
        async with conn.transaction():
            await conn.execute(
                query, 
                accommodation.category, 
                accommodation.city, 
                accommodation.address, 
                accommodation.price_per_night, 
                accommodation.owner
            )
        return {"message": "Acomodação adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar a acomodação: {str(e)}")
    finally:
        await conn.close()

# 1. Listing all accommodations
@api.get("/api/v1/accommodations", response_model=List[Accommodation])
async def list_accommodations():
    conn = await get_database()
    try:
        query = "SELECT * FROM accommodation"
        rows = await conn.fetch(query)
        accommodations = [dict(row) for row in rows]
        return accommodations
    finally:
        await conn.close()

# 2. Adding a new accommodation
async def exits_accommodation(address: str, owner: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM accommodation WHERE LOWER(owner) = LOWER($1) AND LOWER(owner) = LOWER($2)"
        result = await conn.fetchval(query, address, owner)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se a acomodação existe: {str(e)}")

@api.post("/api/v1/accommodations", status_code=201)
async def adding_accommodation(accommodation: AccommodationBase):
    conn = await get_database()
    if await exits_accommodation(accommodation.address, accommodation.owner, conn):
        raise HTTPException(status_code=400, detail="A Acomodação já existe.")
    try:
        query = "INSERT INTO accommodation (category, city, address, price_per_night, owner) VALUES ($1, $2, $3, $4, $5)"
        async with conn.transaction():
            result = await conn.execute(query, accommodation.category, accommodation.city, accommodation.address, accommodation.price_per_night, accommodation.owner)
            return {"message": "Acomodação adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar a acomodação: {str(e)}")
    finally:
        await conn.close()

# 3. Updating an accommodation
@api.patch("/api/v1/accommodations/{accommodation_id}")
async def update_accommodation(accommodation_id: int, accommodation_update: AccommodationUpdate):
    conn = await get_database()
    try:
        # Verify if the accommodation exists
        query = "SELECT * FROM accommodation WHERE id = $1"
        accommodation = await conn.fetchrow(query, accommodation_id)
        if accommodation is None:
            raise HTTPException(status_code=404, detail="Acomodação não encontrada.")

        # Update the accommodation
        update_query = """
        UPDATE accommodation
        SET category = COALESCE($1, category),
            city = COALESCE($2, city),
            address = COALESCE($3, address),
            price_per_night = COALESCE($4, price_per_night),
            owner = COALESCE($5, owner)
        WHERE id = $6
        """
        await conn.execute(
            update_query,
            accommodation_update.category,
            accommodation_update.city,
            accommodation_update.address,
            accommodation_update.price_per_night,
            accommodation_update.owner,
            accommodation_id
        )
        return {"message": "Acomodação atualizada com sucesso!"}
    finally:
        await conn.close()

# 4. Remove an accommodation
@api.delete("/api/v1/accommodations/{accommodation_id}")
async def delete_accommodation(accommodation_id: int):
    conn = await get_database()
    try:
        # Verify if the accommodation exists
        query = "SELECT * FROM accommodation WHERE id = $1"
        accommodation = await conn.fetchrow(query, accommodation_id)
        if accommodation is None:
            raise HTTPException(status_code=404, detail="Acomodação não encontrada.")

        # Remove the accommodation
        delete_query = "DELETE FROM accommodation WHERE id = $1"
        await conn.execute(delete_query, accommodation_id)
        return {"message": "Acomodação removida com sucesso!"}
    finally:
        await conn.close()

@api.delete("/api/v1/accomodations")
async def reset_accommodation():
    init_sql = os.getenv("INIT_SQL", "database/init-db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

# 5. Listing distinct categories
@api.get("/api/v1/accommodations/categories", response_model=List[str])
async def get_distinct_categories():
    conn = await get_database()
    try:
        # Consulta para pegar categorias distintas
        query = "SELECT DISTINCT category FROM accommodation"
        rows = await conn.fetch(query)
        
        # Extrair apenas as categorias
        categories = [row["category"] for row in rows]
        return categories
    finally:
        await conn.close()

# 8. Endpoint para listar acomodações de uma categoria específica
@api.get("/api/v1/accommodations/category", response_model=List[Accommodation])
async def list_accommodations_by_category(category: str):
    conn = await get_database()
    try:
        # Consulta para pegar as acomodações pela categoria
        query = "SELECT * FROM accommodation WHERE category = $1"
        rows = await conn.fetch(query, category)  # $1 é o parâmetro da consulta
        accommodations = [dict(row) for row in rows]
        
        if not accommodations:
            raise HTTPException(status_code=404, detail="No accommodations found for this category")
        
        return accommodations
    finally:
        await conn.close()
# ----------------- Booking -----------------

# 5. Adding a new booking
async def calculate_total_price(conn, accommodation_id: int, checkin: str, checkout: str) -> float:
    # Buscar o preço por noite da acomodação
    query = "SELECT price_per_night FROM accommodation WHERE id = $1"
    accommodation = await conn.fetchrow(query, accommodation_id)

    if not accommodation:
        raise HTTPException(status_code=404, detail="Acomodação não encontrada.")

    # Calcular a diferença de dias entre checkin e checkout
    nights = (checkout - checkin).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="A duração da estadia deve ser de pelo menos uma noite.")

    # Calcular o preço total
    price_per_night = accommodation["price_per_night"]
    total_price = price_per_night * nights

    return total_price        

@api.post("/api/v1/bookings", status_code=201)
async def add_booking(booking: BookingBase):
    conn = await get_database()
    try:
        if booking.checkout <= booking.checkin:
            raise HTTPException(status_code=400, detail="Checkout deve ser posterior ao checkin.")
        
        # Verificação de disponibilidade
        query_check_availability = """
            SELECT 1
            FROM booking
            WHERE accommodation_id = $1
            AND (
                (checkin <= $2 AND checkout > $2)  -- Caso a data de checkin da nova reserva sobreponha
                OR
                (checkin < $3 AND checkout >= $3)  -- Caso a data de checkout da nova reserva sobreponha
                OR
                (checkin >= $2 AND checkout <= $3) -- Caso a nova reserva sobreponha o período inteiro
            )
            LIMIT 1;
        """
        # Verificar se já existe uma reserva no período solicitado
        existing_booking = await conn.fetchval(query_check_availability, 
                                                booking.accommodation_id, booking.checkin, booking.checkout)
        
        if existing_booking:
            raise HTTPException(status_code=400, detail="As datas solicitadas estão indisponíveis para esta acomodação.")

        # Calculate total price
        total_price = await calculate_total_price(conn, booking.accommodation_id, booking.checkin, booking.checkout)

        query = """
            INSERT INTO booking (accommodation_id, name, total_price, checkin, checkout)
            VALUES ($1, $2, $3, $4, $5)
        """
        await conn.execute(query, booking.accommodation_id, booking.name, total_price, booking.checkin, booking.checkout)
        return {"message": "Reserva criada com sucesso!", "total_price": total_price}
    finally:
        await conn.close()

# 6. List all bookings
@api.get("/api/v1/bookings", response_model=List[Booking])
async def list_bookings():
    conn = await get_database()
    try:
        query = "SELECT * FROM booking"
        rows = await conn.fetch(query)
        bookings = [dict(row) for row in rows]
        return bookings
    finally:
        await conn.close()

# 6. Update a booking
@api.patch("/api/v1/bookings/{booking_id}")
async def update_booking(booking_id: int, booking_update: BookingUpdate):
    conn = await get_database()
    try:
        # Verificar se a reserva existe
        query = "SELECT * FROM booking WHERE id = $1"
        booking = await conn.fetchrow(query, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")

        # Atualizar apenas os campos fornecidos
        update_query = """
            UPDATE booking
            SET 
                accommodation_id = COALESCE($1, accommodation_id),
                name = COALESCE($2, name),
                total_price = COALESCE($3, total_price),
                checkin = COALESCE($4, checkin),
                checkout = COALESCE($5, checkout)
            WHERE id = $6
        """
        await conn.execute(
            update_query,
            booking_update.accommodation_id,
            booking_update.name,
            booking_update.total_price,
            booking_update.checkin,
            booking_update.checkout,
            booking_id
        )
        return {"message": "Reserva atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar a reserva: {str(e)}")
    finally:
        await conn.close()

# 7. Delete a booking  
@api.delete("/api/v1/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    conn = await get_database()
    try:
        query = "DELETE FROM booking WHERE id = $1"
        result = await conn.execute(query, booking_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")
        return {"message": "Reserva cancelada com sucesso!"}
    finally:
        await conn.close()

@api.delete("/api/v1/bookings")
async def reset_booking():
    init_sql = os.getenv("INIT_SQL", "database/init-db/init.sql")
    conn = await get_database()
    try:
        # Read SQL file contents
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        # Execute SQL commands
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)