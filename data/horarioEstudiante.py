
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
from data.clase import dict_clasee


def get_horarioEstudiantee():
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


def get_horarioEstudiantees(id_estudiante):
    
    sql = text(
        f"select clases.id, clases.nrc, clases.nombre, clases.academico, clases.facultad, clases.campus, clases.edificio, clases.aula, clases.lunes, clases.martes, clases.miercoles, clases.jueves, clases.viernes, clases.sabado from horarioEstudiantes inner join clases on horarioEstudiantes.id_clase=clases.id inner join estudiantes on estudiantes.id = horarioEstudiantes.id_estudiante where horarioEstudiantes.id_estudiante='{id_estudiante}'")
            
    result = conn.execute(sql).fetchall()
    if result:
        horario_list = []
        for row in result:
            clase = dict_clasee(row)
            horario_list.append(clase)
        print(horario_list)
        logging.info(f"Se obtuvo información de todas las clases")
        return horario_list
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)