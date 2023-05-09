
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

from data.horarioEstudiante import get_horarioEstudiantee, get_horarioEstudiantees

horarioEstudiateRouter = APIRouter()


@horarioEstudiateRouter.get("/horarioEstudiante", response_model=List[HorarioEstudiante])
def get_horarioEstudiante():
    try:
        with engine.connect() as conn:
            return get_horarioEstudiantee()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@horarioEstudiateRouter.get("/horarioEstudiante/horarioEstudiante/{id_estudiante}", response_model=List[Clase])
def get_HorarioEstudiante_by_Estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            return get_horarioEstudiantees(id_estudiante)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
