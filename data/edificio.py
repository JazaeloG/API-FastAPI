
from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from sqlalchemy.sql import text
from models.edificio import edificios
from schemas.edificio import Edificio

def get_edificioo():
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