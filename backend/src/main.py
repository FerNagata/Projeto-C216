from fastapi import status
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import time
from models import Accommodation, Booking
import src.database.repository as repository 

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/jogos") 
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

@api.get("/accommodation/get-all", status_code=status.HTTP_200_OK, response_description="Get all accommodations")
def get_all_accommodation():
    try:
        response = repository.get_all_accomodation()

        return response
        
    except Exception as e:
        print("Error: ${e}")
        raise HTTPException(status_code=500)

# Adding a new accommodation
@api.post("/api/v1/accomodation", status_code=201)
async def add_accommodation(accomodation: Accommodation):
    conn = await get_database()
    if await get_all_accommodation(accomodation.id, conn):
        raise HTTPException(status_code=400, detail="A acomodação já existe.")
    try:
        query = "INSERT INTO accommodation (category, city, address, price_per_night, owner) VALUES ($1, $2, $3, $4, $5)"
        async with conn.transaction():
            result = await conn.execute(query, accomodation.nome, accomodation.criador, accomodation.pais_origem, accomodation.idioma, accomodation.quantidade, accomodation.preco)
            return {"message": "Acomodação adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar o jogo: {str(e)}")
    finally:
        await conn.close()


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)