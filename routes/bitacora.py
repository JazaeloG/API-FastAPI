
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
from models.docente import docentes
from schemas.docente import Docente

from models.bitacora import bitacoras
from schemas.bitacora import Bitacora

from datetime import datetime



bitacoraRouter = APIRouter()


@bitacoraRouter.get("/bitacora", response_model=List[Bitacora])
def get_bitacora():
    try:
        with engine.connect() as conn:
            result = conn.execute(bitacoras.select()).fetchall()
            print(result)
            bitacora_list = []
            for row in result:
                bitacora_dict = {
                    "id": row[0],
                    "id_clase": row[1],
                    "id_estudiante": row[2],
                    "id_docente": row[3],
                    "tipo": row[4],
                    "hora": row[5]
                }

                bitacora = Bitacora(**bitacora_dict)
                bitacora_list.append(bitacora)
            if result:
                logging.info(
                    f"Se obtuvo información de las bitacoras")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las bitacoras ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/bitacora/{id_clase}", response_model=Bitacora)
def get_bitacora_by_id(id_clase: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(bitacoras.select().where(
                bitacoras.c.id_clase == id_clase)).first()

            if result:
                bitacora_dict = {
                    "id": result[0],
                    "id_clase": result[1],
                    "id_estudiante": result[2],
                    "id_docente": result[3],
                    "tipo": result[4],
                    "hora": result[5]
                }
                bitacora = Bitacora(**bitacora_dict)
                logging.info(
                    f"Se obtuvo información bitacora de la clase con el ID: {id_clase}")
                return docente
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información del docente con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.post("/bitacora")
def registrar_entrada(id_user: str, id_aula: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(estudiantes.select().where(
                estudiantes.c.matricula == id_user)).first()

            new_bitacora = Bitacora
            if result is not None:
                print("alumno")
                new_bitacora.id_estudiante = result.id
            else:
                result = conn.execute(docentes.select().where(
                docentes.c.id == id_user)).first()
            if result is not None:
                print("docente")
                new_bitacora.id_docente = result.id

            if result is None:
                return Response(status_code=HTTP_204_NO_CONTENT)
            
            hora_actual = datetime.now().time()
            print("La hora actual es:", hora_actual)
            print(result)

    except Exception as exception_error:
        logging.error(
            f"Error al crear la clase  ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)
