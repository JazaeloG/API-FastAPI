
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


from data.clase import dict_clasee
from datetime import datetime


def get_horarioAulaas():
    result = conn.execute(horarioAulas.select()).fetchall()
    
    horario_list = []
    for row in result:
        horario_dict = {
            "id": row[0],
            "id_aula": row[1],
            "id_clase": row[2]
        }
        print(horario_dict)
        horario = HorarioAula(**horario_dict)
        print(horario)
        horario_list.append(horario_dict)

    if (result):
        logging.info(f"Se obtuvo información de todas las clases")
        return horario_list
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)


def get_id_horarioAulaa(id_aula):
    sql = text(
        f"select clases.id, clases.nrc, clases.nombre, clases.academico, clases.facultad, clases.campus, clases.edificio, clases.aula, clases.lunes, clases.martes, clases.miercoles, clases.jueves, clases.viernes, clases.sabado from horarioAulas inner join clases on horarioAulas.id_clase=clases.id inner join aulas on aulas.id = horarioAulas.id_aula where horarioAulas.id_aula='{id_aula}'")
    result = conn.execute(sql).fetchall()
    print(result)
    if result:
        clases_list = []
        for row in result:
            clase = dict_clasee(row)
            clases_list.append(clase)
        print(clases_list)
        logging.info(f"Se obtuvo información de todas las clases")
        return clases_list
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)


def get_aula_hour_HorarioAulaa(id_aula):
    sql = text(
        f"select clases.id, clases.nrc, clases.nombre, clases.academico, clases.facultad, clases.campus, clases.edificio, clases.aula, clases.lunes, clases.martes, clases.miercoles, clases.jueves, clases.viernes, clases.sabado from horarioAulas inner join clases on horarioAulas.id_clase=clases.id inner join aulas on aulas.id = horarioAulas.id_aula where horarioAulas.id_aula='{id_aula}'")

    result = conn.execute(sql).fetchall()
    ahora = datetime.now()
    dia_semana_num = ahora.weekday()
    dias_semana = ['lunes', 'martes', 'miercoles',
        'jueves', 'viernes', 'sabado', 'domingo']
    dia_semana_nombre = dias_semana[dia_semana_num] #dia real
    #dia_semana_nombre = "lunes" # dia de prueba

    if result:
        clases_list = []
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
            dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']

            for i in range(len(dias_semana)):
                if row[8+i] is not None:
                    clase_dict[dias_semana[i]] = row[8+i]

            if (dia_semana_nombre in clase_dict):

                limites_dia = clase_dict[dia_semana_nombre]
                            
                hora_inicio_str, hora_fin_str = limites_dia.split("-")
                hora_inicio = datetime.strptime(
                    hora_inicio_str, "%H:%M")
                hora_inicio = hora_inicio.strftime('%H:%M')
                hora_fin = datetime.strptime(hora_fin_str, "%H:%M")
                hora_fin = hora_fin.strftime('%H:%M')
                ahora_time = ahora.strftime('%H:%M')
                print(ahora_time) # hora real
                #ahora_time = "11:00"  # hora de prueba
                ahora_time = datetime.strptime(ahora_time, '%H:%M')
                ahora_time = ahora_time.strftime('%H:%M')
                # Verificar si la hora actual está dentro del rango de tiempo
                if hora_inicio <= ahora_time <= hora_fin:
                                
                    clase = Clase(**clase_dict)
                    clases_list.append(clase)

                    
        if (len(clases_list) == 0):
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            logging.info(f"Se obtuvo información de todas las clases")
            return clases_list
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)
