from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from models.aula import aulas
from schemas.aula import Aula
from data.aula import get_aulas

aulaRouter = APIRouter()


@aulaRouter.get("/aula", response_model=List[Aula])
def get_aula():
    try:
        with engine.connect() as conn:
            return get_aulas()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los edificios ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
