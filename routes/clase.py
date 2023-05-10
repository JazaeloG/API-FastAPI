
from xmlrpc.client import SERVER_ERROR
from uvirtual.uv_library.bot.horario import get_class_uv
import logging
from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante, EstudianteAuth
from models.clase import clases
from schemas.clase import Clase
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from functions_jwt import write_token, validate_token
from werkzeug.security import generate_password_hash, check_password_hash
import json

from sqlalchemy.sql import text

from models.horarioEstudiante import horarioEstudiantes
from schemas.horarioEstudiante import HorarioEstudiante
from models.aula import aulas
from schemas.aula import Aula
from models.edificio import edificios
from schemas.edificio import Edificio

from models.horarioAula import horarioAulas
from schemas.horarioAula import HorarioAula



from data.clase import get_clasees, get_id_clasees, crear_clasees, ingresar_clasees

claseRouter = APIRouter()


@claseRouter.get("/clases", response_model=List[Clase])
def get_clases():
    try:
        with engine.connect() as conn:
            return get_clasees()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@claseRouter.get("/clases/clases/{id_clases}", response_model=Clase)
def get_clase_by_id_clase(id_clase: int):
    try:
        with engine.connect() as conn:
            return get_id_clasees(id_clase)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información del estudiante con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@claseRouter.post("/clases")
def create_clase(data_clase: Clase):
    try:
        with engine.connect() as conn:
            return crear_clasees(data_clase)
            
    except Exception as exception_error:
        logging.error(
            f"Error al crear la clase  ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)


@claseRouter.post("/clase", status_code=HTTP_201_CREATED)
def clases_ingresar_al_sistema(estudiantes_auth: EstudianteAuth):
    try:
        with engine.connect() as conn:
            return ingresar_clasees(estudiantes_auth)

    except Exception as exception_error:
        logging.error(
            f"Error al crear la clase ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
