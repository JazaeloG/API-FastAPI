
from xmlrpc.client import SERVER_ERROR
from uvirtual.uv_library.bot.login import get_user_uv
import logging
from config.db import conn, engine
from models.estudiante import estudiantes
from schemas.estudiante import Estudiante, EstudianteAuth
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from typing import List
from functions_jwt import write_token, validate_token
from werkzeug.security import generate_password_hash, check_password_hash
import json



from data.estudiante import get_estudiantee, get_estudiantees, create_estudiantee
estudianteRouter = APIRouter()


@estudianteRouter.get("/estudiantes", response_model=List[Estudiante])
def get_estudiantes():
    try:
        with engine.connect() as conn:
            return get_estudiantees()
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los estudiantes ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@estudianteRouter.get("/estudiante/estudiante/{id_estudiante}", response_model=Estudiante)
def get_estudiante_by_id_estudiante(id_estudiante: int):
    try:
        with engine.connect() as conn:
            
            return get_estudiantee(id_estudiante)
            
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información del estudiante con el ID : {id_estudiante} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@estudianteRouter.post("/estudiantes")
def create_estudiante(data_estudiante: Estudiante):
    try:
        with engine.connect() as conn:

            return create_estudiantee(data_estudiante)
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        return Response(status_code=SERVER_ERROR)


@estudianteRouter.post("/estudiante", status_code=HTTP_201_CREATED)
def estudiantes_ingresar_al_sistema(estudiantes_auth: EstudianteAuth):
    try:
        with engine.connect() as conn:
            if (estudiantes_auth.correo != None):
                result = conn.execute(estudiantes.select().where(
                    estudiantes.c.correo == estudiantes_auth.correo)).first()
            if (estudiantes_auth.matricula != None):
                result = conn.execute(estudiantes.select().where(
                    estudiantes.c.matricula == estudiantes_auth.matricula)).first()

            if result != None:
                print(result)
                check_passw = check_password_hash(result[2], estudiantes_auth.contraseña)
                if check_passw:
                    return {
                        "status": 200,
                        "message": "Access success",
                        "token": write_token(estudiantes_auth.dict()),
                        "user": get_estudiante_by_id_estudiante(result[0])
                    }
                else:
                    return Response(status_code=HTTP_401_UNAUTHORIZED)

            if (result == None):
                print(result)
                if (estudiantes_auth.matricula != None):
                    student_by_miuv = get_user_uv(user=estudiantes_auth.matricula, password=estudiantes_auth.contraseña)
                    student_dic = json.loads(student_by_miuv)

                    if "nombre" in student_dic:
                        with engine.connect() as conn:
                            new_estudiante = Estudiante
                            new_estudiante.nombre = student_dic["nombre"]
                            new_estudiante.telefono = student_dic["residence_information"]["teléfono"]
                            new_estudiante.foto_perfil = student_dic["student_photo_profile"]
                            new_estudiante.correo = student_dic["personal_information"]["correo_institucional"]
                            new_estudiante.campus = student_dic["academic_information"]["campus"]
                            new_estudiante.semestre = int(
                                student_dic["academic_information"]["periodos_cursados"])
                            new_estudiante.matricula = estudiantes_auth.matricula
                            new_estudiante.contraseña = generate_password_hash(estudiantes_auth.contraseña, "pbkdf2:sha256:30", 30)

                            # result_create = conn.execute(estudiantes.insert().values(new_estudiante))

                            result_create = conn.execute(estudiantes.insert().values(
                                matricula=estudiantes_auth.matricula,
                                contraseña=generate_password_hash(estudiantes_auth.contraseña, "pbkdf2:sha256:30", 30),
                                nombre=student_dic["nombre"],
                                correo=student_dic["personal_information"]["correo_institucional"],
                                campus=student_dic["academic_information"]["campus"],
                                semestre=int(
                                    student_dic["academic_information"]["periodos_cursados"]),
                                telefono=student_dic["residence_information"]["teléfono"],
                                foto_perfil=student_dic["student_photo_profile"],
                            ))
                            conn.commit()
                            logging.info(
                                f"Estudiante {new_estudiante.nombre} creado correctamente")
                            if result_create:
                                return {
                                    "status": 200,
                                    "message": "Access success",
                                    "token": write_token(estudiantes_auth.dict()),
                                    "user": result_create
                                }
                            else:
                                return {
                                    "status": 404,
                                    "message": "User not found",
                                }

                else:
                    return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(f"Error al crear información del estudiante ")
        return {
            "status": 404,
            "message": "User not found",
        }


@estudianteRouter.post("/estudiante/verify/token")
def estudiantes_verificar_token(token_estudiante: str = Header(default=None)):
    # token = user_token.split(' ')[1]
    token = token_estudiante.split(" ")[0]
    return validate_token(token_estudiante, output=True)
