
from xmlrpc.client import SERVER_ERROR
from uvirtual.uv_library.bot.horario  import get_user_uv
import logging
from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante, EstudianteAuth
from models.clase import clases
from schemas.clase import Clase
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED
from typing import List
from functions_jwt import write_token, validate_token
from werkzeug.security import generate_password_hash, check_password_hash
import json
from pydantic import BaseModel

claseRouter = APIRouter()


@claseRouter.get("/clases", response_model=List[Clase])
def get_clases():
    try:
        with engine.connect() as conn:
            result = conn.execute(clases.select()).fetchall()
            clases_list = []
            for row in result:
                clase_dict = {
                    "id": row[0],
                    "nrc": row[1],
                    "nombre": row[2],
                    "academico": row[3],
                    "facultad": row[4],
                    "campus": row[5],
                    "edificio": row[6],
                    "aula": row[7]
                }
                dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']

                for i in range(len(dias_semana)):
                    if row[8+i] is not None:
                        clase_dict[dias_semana[i]] = row[8+i]
                
                clase = Clase(**clase_dict)
                clases_list.append(clase)
            
             # Iterar sobre la lista de estudiantes e imprimir cada uno de ellos
            for clase in clases_list:
                print(clase.dict())
            
        if(result):
            logging.info(f"Se obtuvo información de todas las clases")
            return clases_list
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información de las clases ||| {exception_error}") 
        return Response(status_code= SERVER_ERROR )
   
@claseRouter.get("/clases/clases/{id_clases}", response_model=Clase)
def get_clase_by_id_clase(id_clase: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(clases.select().where(clases.c.id == id_clase)).first()
            print(result)
            clase_dict = {
                "id": result[0],
                "nrc": result[1],
                "nombre": result[2],
                "academico": result[3],
                "facultad": result[4],
                "campus": result[5],
                "edificio": result[6],
                "aula": result[7]
            }
            dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']

            for i in range(len(clase_dict)-len(dias_semana)):
                if result[8+i] is not None:
                    clase_dict[dias_semana[i]] = result[8+i]
            
            clase = Clase(**clase_dict)
            if result:
                logging.info(f"Se obtuvo información de la clase con el ID: {id_clase}")
                return clase
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al obtener información del estudiante con el ID : {id_clase} ||| {exception_error}") 
        return Response(status_code=SERVER_ERROR)




@claseRouter.post("/clases")
def create_clase(data_clase: Clase):
    try:
        with engine.connect() as conn:
            
            result = conn.execute(clases.select().where(clases.c.nrc == data_clase.nrc)).first()    
            
            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
            
            new_clase = data_clase.dict()
            conn.execute(clases.insert().values(new_clase))
            conn.commit()
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        return Response(status_code= SERVER_ERROR )

@claseRouter.post("/clase", status_code=HTTP_201_CREATED)
def clases_ingresar_al_sistema(estudiantes_auth : EstudianteAuth):
    
    with engine.connect() as conn:  
        if(estudiantes_auth.correo != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.correo == estudiantes_auth.correo )).first()
        if(estudiantes_auth.matricula != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.matricula == estudiantes_auth.matricula )).first()
        
        if result != None:
            
            check_passw = check_password_hash(result[2], estudiantes_auth.contraseña)
            if check_passw:
                class_by_miuv = get_user_uv(user=estudiantes_auth.matricula,password=estudiantes_auth.contraseña)
                class_dict = json.loads(class_by_miuv)
                print(class_by_miuv)
                print(":::::::::::::::::::::::::::::::::::")
                dic = class_dict['clases']
                for clase, detalles in dic.items():
                    
                    print("\n\n")
                    nrc = detalles["detalles"].get("nrc")
                                        
                    if nrc is not None:

                        result = conn.execute(clases.select().where(clases.c.nrc == nrc)).first()
                        if (result==None):
                            new_clase = Clase
                            new_clase.nrc = detalles["detalles"]["nrc"]
                            new_clase.nombre = clase
                            new_clase.academico = detalles["general"]["acad"]
                            new_clase.facultad = detalles["general"]["escuela"]
                            new_clase.campus = str(detalles["detalles"]["campus"])
                            new_clase.edificio = str(detalles["general"]["edificio"])
                            
                            new_clase.aula = str(detalles["general"]["aula"])

                            dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']
                            dias_dict = {}
                            for dia in dias_semana:
                                if dia in detalles["general"]:
                                    dia_str = str(detalles["general"][dia])
                                    dias_dict[dia] = dia_str
                                   
                            print(dias_dict)
                            result_create = conn.execute(clases.insert().values(
                                nrc = new_clase.nrc,
                                nombre = new_clase.nombre,
                                academico = new_clase.academico,
                                facultad = new_clase.facultad,
                                campus = new_clase.campus,
                                edificio = new_clase.edificio,
                                aula = new_clase.aula,
                                **dias_dict
                            ))
                            #result_create = conn.execute(clases.insert().values(new_clase))
                            conn.commit()
                            logging.info(f"Clase {new_clase.nombre} creada correctamente")
                        
                return {
                "status": 200,
                "message": "Access success",
                "token" : write_token(estudiantes_auth.dict()),
                #"user" : get_estudiante_by_id_estudiante(result[0])
                }
            else:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
        
       
                            
        else:
            return JSONResponse(content={"message": "User not found"}, status_code=404)