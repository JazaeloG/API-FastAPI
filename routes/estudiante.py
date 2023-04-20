# from distutils.log import error
from xmlrpc.client import SERVER_ERROR
# from fastapi import APIRouter, Response, Header
# from fastapi.responses import JSONResponse
# from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
# from werkzeug.security import generate_password_hash, check_password_hash

from config.db import conn, engine
from fastapi import APIRouter
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante


estudianteRouter = APIRouter()


@estudianteRouter.get("/estudiantes")
def get_uestudiantes():
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select()).fetchall()
    except Exception as exception_error:
        return Response(status_code= SERVER_ERROR )
   

@estudianteRouter.post("/estudiantes")
def create_estudiante(data_estudiante: Estudiante):
    with engine.connect() as conn:
        new_estudiante = {
        "matricula": data_estudiante.matricula,
        "contraseña": data_estudiante.contraseña,
        "nombre": data_estudiante.nombre,
        "correo": data_estudiante.correo,
        "semestre": data_estudiante.semestre,
        "campus": data_estudiante.campus,
        "telefono": data_estudiante.telefono,
        "foto_perfil": data_estudiante.foto_perfil
    }

    print(new_estudiante)
#   return conn.execute(estudiantes.select().where(estudiantes.c.id == result.lastrowid)).first()
    result_create=conn.execute(estudiantes.insert().values(
        matricula=data_estudiante.matricula,
        contraseña=data_estudiante.contraseña,
        nombre=data_estudiante.nombre,
        correo=data_estudiante.correo,
        semestre=int(data_estudiante.semestre),
        campus=data_estudiante.campus,
        telefono=str(data_estudiante.telefono)
    ))
    print(result_create)
    print(result_create.lastrowid)
    result = conn.execute(estudiantes.select().where(
    estudiantes.c.id == result_create.lastrowid)).first()
    print(result)

    if result_create:
        return {
            "status": 200,
            "message": "Access success",
        }
    else:
        return {
            "status": 404,
            "message": "User not found"
        }