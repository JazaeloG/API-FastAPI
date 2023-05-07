
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
from models.aula import aulas
from schemas.aula import Aula

aulaRouter = APIRouter()


@aulaRouter.get("/aula", response_model=List[Aula])
def get_aula():
    try:
        with engine.connect() as conn:
            result = conn.execute(aulas.select()).fetchall()
            print(result)
            aula_list = []
            for row in result:
                aula_dict = {
                    "id": row[0],
                    "nombre": row[1],
                    "id_edificio": row[2]
                }
                aula = Aula(**aula_dict)
                aula_list.append(aula_dict)
    
            if (result):
                logging.info(f"Se obtuvo información de todos los edifcios")
                return aula_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los edificios ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
