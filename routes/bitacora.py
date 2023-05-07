
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
from models.docente import docentes
from schemas.docente import Docente

from models.bitacora import bitacoras
from schemas.bitacora import Bitacora

from datetime import datetime



bitacoraRouter = APIRouter()


@bitacoraRouter.get("/bitacora", response_model=List[Bitacora])
def get_bitacora():
    try:
        with engine.connect() as conn:
            result = conn.execute(bitacoras.select()).fetchall()
            print(result)
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
            if result:
                logging.info(
                    f"Se obtuvo información de las bitacoras")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de las bitacoras ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.get("/bitacora/clase/{id_clase}", response_model=List[Bitacora])
def get_bitacora_by_id(id_clase: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(bitacoras.select().where(
                bitacoras.c.id_clase == id_clase)).fetchall()
            print(result)
            if(result):
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
                    f"Se obtuvo información bitacora de la clase con el ID: {id_clase}")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)



@bitacoraRouter.get("/bitacora/dia/{id_clase}/{dia}", response_model=List[Bitacora])
def get_bitacora_by_id(id_clase: int, dia: str):
    try:
        with engine.connect() as conn:

            dia = datetime.strptime(dia, '%Y-%m-%d').date()
            print(dia)
            sql = text(
                f"select * from bitacoras where id_clase='{id_clase}' and DATE(hora)='{dia}'")

            result = conn.execute(sql).fetchall()
            print(result)
            if(result):
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
                    f"Se obtuvo información bitacora de la clase con el ID: {id_clase}")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_clase} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)



@bitacoraRouter.get("/bitacora/aula/{id_aula}", response_model=List[Bitacora])
def get_bitacora_by_id(id_aula: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(bitacoras.select().where(
                bitacoras.c.id_aula == id_aula)).fetchall()
            print(result)
            if(result):
                bitacora_list = []
                for row in result:
                    bitacora_dict = {
                        "id": int(row[0]),
                        "id_aula": int(row[1]),
                        "id_estudiante": row[2],
                        "id_docente": row[3],
                        "id_aula": int(row[4]),
                        "tipo": str(row[5]),
                        "hora": str(row[6])
                    }
                    
                    bitacora = Bitacora(**bitacora_dict)
                    bitacora_list.append(bitacora)
                
                logging.info(
                    f"Se obtuvo información bitacora de la clase con el ID: {id_aula}")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la clase con el ID : {id_aula} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)

@bitacoraRouter.get("/bitacora/dia/{id_aula}/{dia}", response_model=List[Bitacora])
def get_bitacora_by_id(id_aula: int, dia: str):
    try:
        with engine.connect() as conn:

            dia = datetime.strptime(dia, '%Y-%m-%d').date()
            print(dia)
            sql = text(
                f"select * from bitacoras where id_aula='{id_aula}' and DATE(hora)='{dia}'")

            result = conn.execute(sql).fetchall()
            print(result)
            if(result):
                bitacora_list = []
                for row in result:
                    bitacora_dict = {
                        "id": int(row[0]),
                        "id_aula": int(row[1]),
                        "id_estudiante": row[2],
                        "id_docente": row[3],
                        "id_aula": int(row[4]),
                        "tipo": str(row[5]),
                        "hora": str(row[6])
                    }
                    
                    bitacora = Bitacora(**bitacora_dict)
                    bitacora_list.append(bitacora)
                
                logging.info(
                    f"Se obtuvo información bitacora de la aula con el ID: {id_aula}")
                return bitacora_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de la aula con el ID : {id_aula} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@bitacoraRouter.post("/bitacora/{id_user}/{id_aula}/{id_clase}")
def registrar_entrada(id_user: str, id_aula: int, id_clase: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(estudiantes.select().where(
                estudiantes.c.matricula == id_user)).first()

            new_bitacora = Bitacora
            if result is not None:
                new_bitacora.id_estudiante = result.id
                entrada = conn.execute(bitacoras.select().where(bitacoras.c.id_estudiante==result.id and bitacoras.c.id_aula == id_aula).order_by(bitacoras.c.hora.desc())).first()
                tipo= "Student"
            else:
                result = conn.execute(docentes.select().where(
                docentes.c.id == id_user)).first()
                if result is not None:
                    print("docente")
                    new_bitacora.id_docente = result.id
                    entrada = conn.execute(bitacoras.select().where(bitacoras.c.id_docente==result.id and bitacoras.c.id_aula == id_aula).order_by(bitacoras.c.hora.desc())).first()
                    tipo="Docente"
            if result is None:
                return Response(status_code=HTTP_204_NO_CONTENT)
            
            new_bitacora.id_clase=id_clase
            new_bitacora.id_aula=id_aula
            if entrada is None:
                new_bitacora.tipo=str("E")
                print("entro")
            elif entrada.tipo==str("S"):
                new_bitacora.tipo= str("E")
                print("entroa")
            elif entrada.tipo == str("E"):
                new_bitacora.tipo= str("S")
                print("salio")
            print(entrada.tipo)
            new_bitacora.hora = datetime.now()  
            print(new_bitacora.hora)
            print("holi")
            if tipo =="Student":
                result = conn.execute(bitacoras.insert().values(
                    id_clase = new_bitacora.id_clase,
                    id_estudiante = new_bitacora.id_estudiante,
                    id_aula = new_bitacora.id_aula,
                    tipo = new_bitacora.tipo,
                    hora = new_bitacora.hora
                ))
            elif tipo == "Docente":
                result = conn.execute(bitacoras.insert().values(
                    id_clase = new_bitacora.id_clase,
                    id_docente = new_bitacora.id_docente,
                    id_aula = new_bitacora.id_aula,
                    tipo = new_bitacora.tipo,
                    hora = new_bitacora.hora
                ))
            conn.commit()
            return result
    except Exception as exception_error:
        logging.error(
            f"Error al crear la clase  ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)
