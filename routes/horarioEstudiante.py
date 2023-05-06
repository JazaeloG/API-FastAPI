
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

horarioEstudiateRouter = APIRouter()


@horarioEstudiateRouter.get("/horarioEstudiante", response_model=List[HorarioEstudiante])
def get_horarioEstudiante():
    try:
        with engine.connect() as conn:
            result = conn.execute(horarioEstudiantes.select()).fetchall()
            
            horario_list = []
            for row in result:
                horario_dict = {
                    "id": row[0],
                    "id_estudiante": row[1],
                    "clase_id": row[2]
                }

                horario = HorarioEstudiante(**horario_dict)
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


@horarioEstudiateRouter.get("/horarioEstudiante/horarioEstudiante/{id_estudiante}", response_model=List[Clase])
def get_HorarioEstudiante_by_Estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            """result = conn.execute(horarioEstudiantes.select().where(
                horarioEstudiantes.c.id_estudiante == id_estudiante)).fetchall()
            print(result)
            result = conn.execute(horarioEstudiantes.select().join(estudiantes, estudiantes.c.id == horarioEstudiantes.c.id_estudiante).join(
                clases, clases.c.id == horarioEstudiantes.c.id_clase).where(horarioEstudiantes.c.id_estudiante == id_estudiante)).fetchall()

            print(result)"""
            sql = text(
                f"select clases.id, clases.nrc, clases.nombre, clases.academico, clases.facultad, clases.campus, clases.edificio, clases.aula, clases.lunes, clases.martes, clases.miercoles, clases.jueves, clases.viernes, clases.sabado from horarioEstudiantes inner join clases on horarioEstudiantes.id_clase=clases.id inner join estudiantes on estudiantes.id = horarioEstudiantes.id_estudiante where horarioEstudiantes.id_estudiante='{id_estudiante}'")
            
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
