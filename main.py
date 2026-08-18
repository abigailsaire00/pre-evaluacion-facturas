from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Factura(BaseModel):
    id: int | None = None 
    numero_factura: int
    fecha: str
    cliente: str
    total: int

class FacturaCreate(BaseModel):
    numero_factura: int
    fecha: str
    cliente: str
    total: int



origins = [
     "http://localhost:5500",
     "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/facturas")
async def obtenerFacturas() -> list [Factura]:
    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM facturas ORDER BY numero_factura DESC")

    data = respuesta.fetchall()

    conexion.close()
    
    return [dict(factura) for factura in data]


@app.get("/facturas/{id}")
async def obtenerFactura(id: int) -> Factura:

    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM facturas WHERE id=?", (id,))

    data = respuesta.fetchone()

    
    return(dict(data))

@app.post("/facturas")
async def agregarFactura(factura: FacturaCreate):
    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO facturas (numero_factura, fecha, cliente, total) VALUES (?, ?, ?, ?)", (factura.numero_factura, factura.fecha, factura.cliente, factura.total))

    conexion.commit()
    conexion.close()




