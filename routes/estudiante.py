# from distutils.log import error
from xmlrpc.client import SERVER_ERROR
# from fastapi import APIRouter, Response, Header
# from fastapi.responses import JSONResponse
# from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
# from werkzeug.security import generate_password_hash, check_password_hash
import logging
from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante
from fastapi import APIRouter, Response, Header

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED
from typing import List

from library.uv_library.bot.login import get_user_uv

estudianteRouter = APIRouter()


"""
 - Te falto retornar la respuesta del servidor
 return result
"""
@estudianteRouter.get("/estudiantes", response_model=List[Estudiante])
def get_estudiantes():
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select()).fetchall()
            estudiantes_list = []
            for row in result:
                estudiante_dict = {
                    "id": row[0],
                    "matricula": row[1],
                    "contraseña": row[2],
                    "nombre": row[3],
                    "correo": row[4],
                    "campus": row[5],
                    "semestre": row[6],
                    "telefono": row[7],
                    "foto_perfil": row[8],
                }
                estudiante = Estudiante(**estudiante_dict)
                estudiantes_list.append(estudiante)
            
             # Iterar sobre la lista de estudiantes e imprimir cada uno de ellos
            for estudiante in estudiantes_list:
                print(estudiante.dict())
            
        if(result):
            logging.info(f"Se obtuvo información de todos los estudiantes")
            return estudiantes_list
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de los estudiantes ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@estudianteRouter.get("/estudiante/estudiante/{id_estudiante}", response_model=Estudiante)
def get_estudiante_by_id_estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select().where(estudiantes.c.id == id_estudiante)).first()
            estudiante_dict = {
                "id": result[0],
                "matricula": result[1],
                "contraseña": result[2],
                "nombre": result[3],
                "correo": result[4],
                "campus": result[5],
                "semestre": result[6],
                "telefono": result[7],
                "foto_perfil": result[8],
            }
            estudiante = Estudiante(**estudiante_dict)
            if result:
                logging.info(f"Se obtuvo información del estudiante con el ID: {id_estudiante}")
                return estudiante
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del estudiante con el ID : {id_estudiante} ||| {exception_error}") 
        return Response(status_code=SERVER_ERROR)




@estudianteRouter.post("/estudiantes")
def create_estudiante(data_estudiante: Estudiante):
    try:
        with engine.connect() as conn:
            """
            Lo ideal seria verificar si ya existe un estudiante con esa matricula / correo registrado
            antes de crear otro para ello hacemos:
            
            -Seleccionar de la tabla estudiantes, donde ....
                estudiantes.select().where 
            
            -La tabla estuddiantes, de la columna correo
                estudiantes.c.correo
                
            - Es igual a lo que manda el usuario en el objeto data_estudiante en la parte de correo
                == data_estudiante.correo
                
            - o checar si se encuentra la columna  matricula algun registro igual a lo que manda el usuario
                or estudiantes.c.matricula == data_estudiante.matricula
            
            - Si hay registro ya de matricula o de correo la variable result contendrá algo, por lo tanto
                responde el servidor como 401 SIN AUTORIZACIÓN 
            
            - Si no hay registro alguno podemos guardar nuestro registro para ello convertimos lo que el usuario nos manda
            en un diccionario para que al insetar los valos haga la equivalencia del modelo y el esquema
            
                new_estudiante = data_estudiante.dict()
                
            - Y finalmente respondemos un estatus 201 para mostrar que los datos se han guardado correctamente
                return Response(status_code=HTTP_201_CREATED)
            
            
            --- NOta ---
            - Si duante el proceso se presentó algun error retornamos un Error server, esto para que el programador del front 
            pueda consultar los estados al consumir nuestra api rest

            
            """
            result = conn.execute(estudiantes.select().where(estudiantes.c.correo == data_estudiante.correo or estudiantes.c.matricula == data_estudiante.matricula)).first()    
            
            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
            
            new_estudiante = data_estudiante.dict()
            print(new_estudiante)
            conn.execute(estudiantes.insert().values(new_estudiante))
            conn.commit()
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        return Response(status_code= SERVER_ERROR )
