
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
from models.horarioDocente import horarioDocentes
from schemas.horarioDocente import HorarioDocente

horarioDocenteRouter = APIRouter()


@horarioDocenteRouter.get("/horarioDocente", response_model=List[HorarioDocente])
def get_horarioDocente():
    try:
        with engine.connect() as conn:
            result = conn.execute(horarioDocentes.select()).fetchall()
            print(result)
            horario_list = []
            for row in result:
                horario_dict = {
                    "id": row[0],
                    "id_docente": row[1],
                    "id_clase": row[2]
                }
                print(horario_dict)
                horario = HorarioDocente(**horario_dict)
                print(horario)
                horario_list.append(horario_dict)
    
            if (result):
                logging.info(f"Se obtuvo información de todas las clases")
                return horario_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@horarioDocenteRouter.get("/horarioDocente/horarioDocente/{id_docente}", response_model=List[Clase])
def get_HorarioDocente_by_Docente(id_docente: int):
    try:
        with engine.connect() as conn:

            sql = text(
                f"select clases.id, clases.nrc, clases.nombre, clases.academico, clases.facultad, clases.campus, clases.edificio, clases.aula, clases.lunes, clases.martes, clases.miercoles, clases.jueves, clases.viernes, clases.sabado from horarioDocentes inner join clases on horarioDocentes.id_clase=clases.id inner join docentes on docentes.id = horarioDocentes.id_docente where horarioDocentes.id_docente='{id_docente}'")

            result = conn.execute(sql).fetchall()
            if result:
                horario_list = []
                for row in result:
                    clase_dict = {
                        "id": row[0],
                        "nrc": row[1],
                        "nombre": row[2],
                        "academico": row[3],
                        "facultad": row[4],
                        "campus": row[5],
                        "edificio": row[6],
                        "aula": row[7]
                    }
                    dias_semana = ['lunes', 'martes', 'miercoles',
                                   'jueves', 'viernes', 'sabado']

                    for i in range(len(clase_dict)-len(dias_semana)):
                        if row[8+i] is not None:
                            clase_dict[dias_semana[i]] = row[8+i]

                    clase = Clase(**clase_dict)
                    horario_list.append(clase)
                print(horario_list)
                logging.info(f"Se obtuvo información de todas las clases")
                return horario_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las clases ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
