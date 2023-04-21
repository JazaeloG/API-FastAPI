# from distutils.log import error
from xmlrpc.client import SERVER_ERROR
# from fastapi import APIRouter, Response, Header
# from fastapi.responses import JSONResponse
# from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
# from werkzeug.security import generate_password_hash, check_password_hash

from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante
from fastapi import APIRouter, Response, Header

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED


from typing import List
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
            
            return estudiantes_list
    except Exception as exception_error:
        print(".................")
        return Response(status_code= SERVER_ERROR )
   

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
