
from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine 
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
import json
from sqlalchemy.sql import text
from fastapi import APIRouter, Response, Header

from models.bitacora import bitacoras
from schemas.bitacora import Bitacora

from models.docente import docentes
from schemas.docente import Docente
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante

from datetime import datetime



def get_bitacoraa():
    result = conn.execute(bitacoras.select()).fetchall()
    print(result)
    return list_bitacoraa(result)
    

def get_list_bitacoraa(id_clase):
    result = conn.execute(bitacoras.select().where(
                bitacoras.c.id_clase == id_clase)).fetchall()
    print(result)
    return list_bitacoraa(result)


def get_list_day_bitacoraa(id_clase, dia):
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    print(dia)
    sql = text(
        f"select * from bitacoras where id_clase='{id_clase}' and DATE(hora)='{dia}'")
    result = conn.execute(sql).fetchall()
    print(result)
    return list_bitacoraa(result)


def get_list_class_bitacoraa(id_aula):
    result = conn.execute(bitacoras.select().where(
        bitacoras.c.id_aula == id_aula)).fetchall()
    print(result)
    return list_bitacoraa(result)


def get_list_classday_bitacoraa(id_aula, dia):
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    print(dia)
    sql = text(
        f"select * from bitacoras where id_aula='{id_aula}' and DATE(hora)='{dia}'")
    result = conn.execute(sql).fetchall()
    print(result)
    return list_bitacoraa(result)


def list_bitacoraa(result):
    if result:
        bitacora_list = []
        for row in result:
            bitacora_dict = {
                "id": int(row[0]),
                "id_clase": int(row[1]),
                "id_estudiante": row[2],
                "id_docente": row[3],
                "id_aula": int(row[4]),
                "tipo": str(row[5]),
                "hora": str(row[6])
            }
            bitacora = Bitacora(**bitacora_dict)
            bitacora_list.append(bitacora)
        
            logging.info(
                f"Se obtuvo información de las bitacoras")
        return bitacora_list
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)


def set_entrada(id_user, id_aula, id_clase):
    result = conn.execute(estudiantes.select().where(
        estudiantes.c.matricula == id_user)).first()
    dia = datetime.now().date()
    print(dia)
    new_bitacora = Bitacora
    if result is not None:
        new_bitacora.id_estudiante = result.id
        
        id=result.id
        sql = text(
            f"select * from bitacoras where id_clase='{id_clase}' and DATE(hora)='{dia}' and bitacoras.id_estudiante ='{id}' and bitacoras.id_aula = '{id_aula}' order by hora desc")
        #entrada = conn.execute(bitacoras.select().where(bitacoras.c.id_estudiante == result.id and bitacoras.c.id_aula == id_aula).order_by(bitacoras.c.hora.desc())).first()
        entrada = conn.execute(sql).first()
        tipo = "Student"
    else:
        result = conn.execute(docentes.select().where(
            docentes.c.id == id_user)).first()
        if result is not None:
            new_bitacora.id_docente = result.id
            #entrada = conn.execute(bitacoras.select().where(bitacoras.c.id_docente == result.id and bitacoras.c.id_aula == id_aula).order_by(bitacoras.c.hora.desc())).first()
            id=result.id
            sql = text(
                f"select * from bitacoras where id_clase='{id_clase}' and DATE(hora)='{dia}' and bitacoras.id_docente ='{id}' and bitacoras.id_aula = '{id_aula}' order by hora desc")
            entrada = conn.execute(sql).first()
            tipo = "Docente"
    if result is None:
        print("..............................")
        return Response(status_code=HTTP_204_NO_CONTENT)

    new_bitacora.id_clase = id_clase
    new_bitacora.id_aula = id_aula
    if entrada is None:
        new_bitacora.tipo = str("E")
    elif entrada.tipo == str("S"):
        new_bitacora.tipo = str("E")
    elif entrada.tipo == str("E"):
        new_bitacora.tipo = str("S")

    new_bitacora.hora = datetime.now()
    print(new_bitacora.hora)
    if tipo == "Student":
        result = conn.execute(bitacoras.insert().values(
            id_clase=new_bitacora.id_clase,
            id_estudiante=new_bitacora.id_estudiante,
            id_aula=new_bitacora.id_aula,
            tipo=new_bitacora.tipo,
            hora=new_bitacora.hora
        ))
    elif tipo == "Docente":
        result = conn.execute(bitacoras.insert().values(
            id_clase=new_bitacora.id_clase,
            id_docente=new_bitacora.id_docente,
            id_aula=new_bitacora.id_aula,
            tipo=new_bitacora.tipo,
            hora=new_bitacora.hora
            ))
    conn.commit()
    return result