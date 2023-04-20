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

estudianteRouter = APIRouter()


"""
 - Te falto retornar la respuesta del servidor
 return result
"""
@estudianteRouter.get("/estudiantes")
def get_uestudiantes():
    try:
        with engine.connect() as conn:
            result = conn.execute(estudiantes.select()).fetchall()
            print(result)
            print("--------------")
            return result # <--  De lo contrario nunca te devuelve nada
    except Exception as exception_error:
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
            
            #new_estudiante["contrasena"] = generate_password_hash(data_estudiante.contrasena, "pbkdf2:sha256:30", 30)
            conn.execute(estudiantes.insert().values(new_estudiante))
            print(new_estudiante)
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        return Response(status_code= SERVER_ERROR )
