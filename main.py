from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


app = FastAPI()

tems = {"foo": "The Foo Wrestlers"}


 # @app.get("/items/{item_id}")
 # async def read_item(item_id: str):
    
     # if item_id not in items:
         # raise HTTPException(status_code=404, detail="Item not found")
   # return {"item": items[item_id]}

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

class Persona(BaseModel):
    id: int | None = None 
    nombre: str
    apellido: str
    edad: int
    fecha_cumpleaños: str
    color_favorito: str

class PersonasCreate(BaseModel):
        nombre: str
        apellido: str
        edad: int
        fecha_cumpleaños: str
        color_favorito: str

class PersonasUpdate(BaseModel): 
    edad: int

class Alumno(BaseModel):
        id: int | None = None 
        nombre: str
        apellido: str
        curso: str
        correo: str

class AlumnosCreate(BaseModel):
            nombre: str
            apellido: str
            curso: str
            correo: str

class AlumnoUpdate(BaseModel):
          curso: str

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

#GET
@app.get("/facturas")
async def obtenerFacturas() -> list [Factura]:
    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM facturas ORDER BY numero_factura DESC")

    data = respuesta.fetchall()

    conexion.close()
    
    return [dict(factura) for factura in data]


@app.get("/personas")
async def obtenerPersonas() -> list [Persona]:
    conexion = sqlite3.connect("prueba.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM personas ORDER BY nombre DESC;")

    data = respuesta.fetchall()
    
    conexion.close()

    return [dict(persona) for persona in data]

@app.get("/alumnos")
async def obtenerAlumnos() -> list [Alumno]:
    conexion = sqlite3.connect("alumnos.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM alumnos;") #"SELECT * FROM alumnos ORDER BY nombre DESC;"

    data = respuesta.fetchall()
    
    conexion.close()

    return [dict(persona) for persona in data]

#GET ID

@app.get("/facturas/{id}")
async def obtenerFactura(id: int) -> Factura:

    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM facturas WHERE id=?", (id,))

    data = respuesta.fetchone()

    if not data:
         raise HTTPException(status_code=404, detail="factura no encontrada")

    return(dict(data))

@app.get("/personas/{id}")
async def obtenerPersonas(id: int) -> Persona:

    conexion = sqlite3.connect("prueba.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM personas WHERE id=?", (id,))

    data = respuesta.fetchone()

    return(dict(data))

@app.get("/alumnos/{id}")
async def obtenerAlumnos(id: int) -> Alumno:

    conexion = sqlite3.connect("alumnos.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM alumnos WHERE id=?", (id,))

    data = respuesta.fetchone()

    return(dict(data))

#DELETE

@app.delete("/facturas")   
async def eliminarFactura() -> list [Factura]:

 conexion = sqlite3.connect("facturas.db")
 conexion.row_factory = sqlite3.Row

 cursor = conexion.cursor()

 respuesta = cursor.execute("DELETE FROM facturas WHERE id=5;")

 conexion.commit()

 data = respuesta.fetchone()

 conexion.close()
 
#return [dict(factura) for factura in data]

@app.delete("/alumnos")   
async def eliminarAlumno() -> list [Alumno]:

 conexion = sqlite3.connect("alumnos.db")
 conexion.row_factory = sqlite3.Row

 cursor = conexion.cursor()

 respuesta = cursor.execute("DELETE FROM alumnos WHERE id=12;")

 conexion.commit()

 data = respuesta.fetchone()

 conexion.close()

#POST

@app.post("/personas")
async def agregarPersona(persona: PersonasCreate):
    conexion = sqlite3.connect("prueba.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO personas (nombre, apellido, edad, fecha_cumpleaños, color_favorito) VALUES (?, ?, ?, ?, ?)", (persona.nombre, persona.apellido, persona.edad, persona.fecha_cumpleaños, persona.color_favorito))

    conexion.commit()
    conexion.close()

    return {"mensaje": "Persona agregada correctamente"}


@app.post("/facturas")
async def agregarFactura(factura: FacturaCreate):
    conexion = sqlite3.connect("facturas.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO facturas (numero_factura, fecha, cliente, total) VALUES (?, ?, ?, ?)", (factura.numero_factura, factura.fecha, factura.cliente, factura.total))

    conexion.commit()
    conexion.close()

@app.post("/alumnos")
async def agregarAlumnos(alumnos: AlumnosCreate):
    conexion = sqlite3.connect("alumnos.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO alumnos (nombre, apellido, curso, correo) VALUES (?, ?, ?, ?)", (alumnos.nombre, alumnos.apellido, alumnos.curso, alumnos.correo))

    conexion.commit()
    conexion.close()
    return {"mensaje": "Alumno agregado correctamente"}

#PUT
@app.put("/personas/{id}")
async def actualizarPersona(id: int, persona: PersonasUpdate):  
    conexion = sqlite3.connect("prueba.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("UPDATE personas SET edad = ? WHERE id = ?", (persona.edad, id))

    conexion.commit()
    conexion.close()

@app.put("/alumnos/{id}")
async def actualizarAlumno(id: int, alumno: AlumnoUpdate):  
    conexion = sqlite3.connect("alumnos.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    cursor.execute("UPDATE alumnos SET curso= ? WHERE id = ?", (alumno.curso, id))

    conexion.commit()
    conexion.close()

    return {"mensaje": "Actualizado correctamente"}

# @app.get("/facturas")
# async def VerificarFactura(id: int) -> Factura:

#     conexion = sqlite3.connect("facturas.db")
#     conexion.row_factory = sqlite3.Row

#     cursor = conexion.cursor()

#     respuesta = cursor.execute("SELECT numero_factura FROM facturas WHERE EXISTS (SELECT 1001 FROM numero_factura WHERE facturas.numero_factura )")

#     data = respuesta.fetchone()

#     return [dict(factura) for factura in data]

    #return(dict(data))


    



    




