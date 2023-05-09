

from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from models.aula import aulas
from schemas.aula import Aula

def get_aulas():
    result = conn.execute(aulas.select()).fetchall()
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