
from xmlrpc.client import SERVER_ERROR
import logging
from config.db import conn, engine
from models.docente import docentes
from schemas.docente import Docente, DocenteAuth, DocenteUpdate
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from functions_jwt import write_token, validate_token
from werkzeug.security import generate_password_hash, check_password_hash
import json

from schemas.estudiante import EstudianteAuth




from data.docente import get_docentee, get_id_docentee, create_docentee, ingresar_docentee, login_docentee, actualizar_docentee

docenteRouter = APIRouter()


@docenteRouter.get("/docentes", response_model=List[Docente])
def get_docentes():
    try:
        with engine.connect() as conn:

            return get_docentee()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los docentes ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.get("/docente/docente/{id_docente}", response_model=Docente)
def get_docente_by_id_docente(id_docente: int):
    try:
        with engine.connect() as conn:

            return get_id_docentee(id_docente)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información del docente con el ID : {id_docente} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.post("/docentes")
def create_docente(data_docente: Docente):
    try:
        with engine.connect() as conn:
            return create_docentee(data_docente)
    except Exception as exception_error:
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)


@docenteRouter.post("/docente", status_code=HTTP_201_CREATED)
def docentes_ingresar_al_sistema(estudiantes_auth: EstudianteAuth):
    try:
        with engine.connect() as conn:
            return ingresar_docentee(estudiantes_auth)
    except Exception as exception_error:
        logging.error(
            f"Error al ingresar docente al sistema ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.put("/docente/{id_docente}", response_model=DocenteUpdate)
def update_docente(data_update: DocenteUpdate, id_docente: int):
    try:
        with engine.connect() as conn:
            return actualizar_docentee(data_update, id_docente)

    except Exception as exception_error:
        logging.error(
            f"Error al actualizar el docente con el ID: {id_docente} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)




@docenteRouter.post("/docente/login", status_code=HTTP_201_CREATED)
def docentes_ingresar_al_sistema(docentes_auth: DocenteAuth):
    try:
        with engine.connect() as conn:
            return login_docentee(docentes_auth)
    except Exception as exception_error:
        logging.error(
            f"Error al ingresar docente al sistema ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)



@docenteRouter.post("/docente/verify/token")
def docentes_verificar_token(token_docente: str = Header(default=None)):
    # token = user_token.split(' ')[1]
    token = token_docente.split(" ")[0]
    return validate_token(token_docente, output=True)
