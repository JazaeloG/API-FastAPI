
from xmlrpc.client import SERVER_ERROR
from uvirtual.uv_library.bot.login  import get_user_uv
import logging
from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante, EstudianteAuth
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED
from typing import List
from functions_jwt import write_token, validate_token
from werkzeug.security import generate_password_hash, check_password_hash
import json
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

@estudianteRouter.post("/estudiante", status_code=HTTP_201_CREATED)
def estudiantes_ingresar_al_sistema(estudiantes_auth : EstudianteAuth):
    
    with engine.connect() as conn:  
        if(estudiantes_auth.correo != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.correo == estudiantes_auth.correo )).first()
        if(estudiantes_auth.matricula != None):
            result = conn.execute(estudiantes.select().where(estudiantes.c.matricula == estudiantes_auth.matricula )).first()
        
        if result != None:
            
            check_passw = check_password_hash(result[2], estudiantes_auth.contraseña)
            if check_passw:
                return {
                "status": 200,
                "message": "Access success",
                "token" : write_token(estudiantes_auth.dict()),
                "user" : get_estudiante_by_id_estudiante(result[0])
                }
            else:
                return Response(status_code=HTTP_401_UNAUTHORIZED)
        
        if(result == None):
            if(estudiantes_auth.matricula != None):
                student_by_miuv = get_user_uv(user=estudiantes_auth.matricula,password=estudiantes_auth.contraseña)
                student_dic = json.loads(student_by_miuv)
                
                if "nombre" in student_dic:
                    with engine.connect() as conn:
                        new_estudiante = Estudiante
                        new_estudiante.nombre =  student_dic["nombre"]
                        new_estudiante.telefono =  student_dic["residence_information"]["teléfono"]
                        new_estudiante.foto_perfil =  student_dic["student_photo_profile"]
                        new_estudiante.correo =  student_dic["personal_information"]["correo_institucional"]
                        new_estudiante.campus =  student_dic["academic_information"]["campus"]
                        new_estudiante.semestre = int(student_dic["academic_information"]["periodos_cursados"])
                        new_estudiante.matricula =  estudiantes_auth.matricula
                        new_estudiante.contraseña = generate_password_hash(estudiantes_auth.contraseña, "pbkdf2:sha256:30", 30)
                        
                        print(new_estudiante)
                        #result_create = conn.execute(estudiantes.insert().values(new_estudiante))
                        
                        result_create = conn.execute(estudiantes.insert().values(                
                            matricula = estudiantes_auth.matricula,
                            contraseña = generate_password_hash(estudiantes_auth.contraseña, "pbkdf2:sha256:30", 30),
                            nombre = student_dic["nombre"],
                            correo = student_dic["personal_information"]["correo_institucional"],
                            campus = student_dic["academic_information"]["campus"],
                            semestre =  int(student_dic["academic_information"]["periodos_cursados"]),
                            telefono = student_dic["residence_information"]["teléfono"],
                            foto_perfil = student_dic["student_photo_profile"],
                        ))
                        conn.commit()
                        logging.info(f"Estudiante {new_estudiante.nombre} creado correctamente")
                        if result_create:
                            return {
                                "status": 200,
                                "message": "Access success",
                                "token" : write_token(estudiantes_auth.dict()),
                                "user" : result_create
                                }
                        else:
                            return {
                                "status": 404,
                                "message": "User not found",
                                }
                            
        else:
            return JSONResponse(content={"message": "User not found"}, status_code=404)