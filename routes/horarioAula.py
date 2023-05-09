
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
from models.horarioAula import horarioAulas
from schemas.horarioAula import HorarioAula

from datetime import datetime


from data.horarioAula import get_horarioAulaas, get_id_horarioAulaa, get_aula_hour_HorarioAulaa
horarioAulaRouter = APIRouter()


@horarioAulaRouter.get("/horarioAula", response_model=List[HorarioAula])
def get_horarioAula():
    try:
        with engine.connect() as conn:
            return get_horarioAulaas
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@horarioAulaRouter.get("/horarioAula/horarioAula/{id_aula}", response_model=List[Clase])
def get_HorarioAula_by_id(id_aula: int):
    try:
        with engine.connect() as conn:
            return get_id_horarioAulaa(id_aula)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@horarioAulaRouter.get("/horarioAula/horarioAulas/{id_aula}", response_model=List[Clase])
def get_HorarioAula_by_id_aula_hour(id_aula: int):
    try:
        with engine.connect() as conn:
            return get_aula_hour_HorarioAulaa(id_aula)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
