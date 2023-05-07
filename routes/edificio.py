
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
from models.edificio import edificios
from schemas.edificio import Edificio

edificioRouter = APIRouter()


@edificioRouter.get("/edificio", response_model=List[Edificio])
def get_Edificio():
    try:
        with engine.connect() as conn:
            result = conn.execute(edificios.select()).fetchall()
            print(result)
            edificio_list = []
            for row in result:
                edificio_dict = {
                    "id": row[0],
                    "nombre": row[1],
                    "facultad": row[2],
                    "campus": row[3]
                }
                edificio = Edificio(**edificio_dict)
                
                edificio_list.append(edificio_dict)
    
            if (result):
                logging.info(f"Se obtuvo información de todos los edifcios")
                return edificio_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los edificios ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
