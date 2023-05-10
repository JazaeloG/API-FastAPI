
from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
import json
from sqlalchemy.sql import text
from models.bitacora import bitacoras
from schemas.bitacora import Bitacora


from data.bitacora import get_bitacoraa, get_list_bitacoraa, get_list_day_bitacoraa, get_list_class_bitacoraa, get_list_classday_bitacoraa, set_entrada


bitacoraRouter = APIRouter()


@bitacoraRouter.get("/bitacora", response_model=List[Bitacora])
def get_bitacora():
    try:
        with engine.connect() as conn:
            return get_bitacoraa()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las bitacoras ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/clase/{id_clase}", response_model=List[Bitacora])
def get_bitacora_by_id(id_clase: int):
    try:
        with engine.connect() as conn:
            return get_list_bitacoraa(id_clase)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/class/dia/{id_clase}/{dia}", response_model=List[Bitacora])
def get_bitacora_by_id(id_clase: int, dia: str):
    try:
        with engine.connect() as conn:
            print("clase y dia")
            return get_list_day_bitacoraa(id_clase, dia)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/aula/{id_aula}", response_model=List[Bitacora])
def get_bitacora_by_id(id_aula: int):
    try:
        with engine.connect() as conn:
            return get_list_class_bitacoraa(id_aula)
            
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_aula} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/dia/{id_aula}/{dia}", response_model=List[Bitacora])
def get_bitacora_by_id_day(id_aula: int, dia: str):
    try:
        with engine.connect() as conn:
            print("aula y dia")
            return get_list_classday_bitacoraa(id_aula, dia)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la aula con el ID : {id_aula} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.post("/bitacora/{id_user}/{id_aula}/{id_clase}")
def registrar_entrada(id_user: str, id_aula: int, id_clase: int):
    try:
        with engine.connect() as conn:
            return set_entrada(id_user, id_aula, id_clase)
    except Exception as exception_error:
        logging.error(
            f"Error al crear la clase  ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)
