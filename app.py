from fastapi import FastAPI
from routes.estudiante import estudianteRouter
from routes.edificio import edificioRouter
from routes.aula import aulaRouter
from routes.clase import claseRouter
from routes.docente import docenteRouter
from routes.horarioEstudiante import horarioEstudiateRouter
from routes.horarioDocente import horarioDocenteRouter
from routes.horarioAula import horarioAulaRouter

from routes.bitacora import bitacoraRouter

from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="REST API to UVirtual by UV",
    description="By ISW UV",
    version="0.1",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudianteRouter, prefix='/api/v1', tags=["Estudiantes"])
app.include_router(claseRouter, prefix='/api/v1', tags=["Clases"])
app.include_router(docenteRouter, prefix='/api/v1', tags=["Docentes"])
app.include_router(horarioEstudiateRouter, prefix='/api/v1',
                   tags=["Horario Estudiante"])
app.include_router(horarioDocenteRouter, prefix='/api/v1',
                   tags=["Horario Docente"])
app.include_router(edificioRouter, prefix='/api/v1', tags=["Edificio"])
app.include_router(aulaRouter, prefix='/api/v1', tags=["Aula"])
app.include_router(horarioAulaRouter, prefix='/api/v1', tags=["Aula"])


app.include_router(bitacoraRouter, prefix='/api/v1', tags=["Bitacoras"])
app.include_router(horarioAulaRouter, prefix='/api/v1', tags=["Aula"])

if __name__ == "__main__":
    # uvicorn.run(app, port=8080, host="0.0.0.0")
    uvicorn.run(app, port=8080, host="127.0.0.1")
