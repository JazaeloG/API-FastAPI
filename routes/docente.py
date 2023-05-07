
from xmlrpc.client import SERVER_ERROR
from uvirtual.uv_library.bot.horario import get_class_uv
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

from models.clase import clases
from schemas.clase import Clase


from models.estudiante import estudiantes
from schemas.estudiante import Estudiante, EstudianteAuth


from models.horarioDocente import horarioDocentes
from schemas.horarioDocente import HorarioDocente


docenteRouter = APIRouter()


@docenteRouter.get("/docentes", response_model=List[Docente])
def get_docentes():
    try:
        with engine.connect() as conn:
            result = conn.execute(docentes.select()).fetchall()
            if (result):
                docentes_list = []
                for row in result:
                    docente_dict = {
                        "id": row[0],
                        "contraseña": row[1],
                        "nombre": row[2],
                        "correo": row[3],
                        "campus": row[4],
                        "telefono": row[5],
                        "foto_perfil": row[6]
                    }
                    docente = Docente(**docente_dict)
                    docentes_list.append(docente)
                logging.info(f"Se obtuvo información de todos los docentes")
                return docentes_list
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información de los docentes ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.get("/docente/docente/{id_docente}", response_model=Docente)
def get_docente_by_id_docente(id_docente: int):
    try:
        with engine.connect() as conn:

            result = conn.execute(docentes.select().where(
                docentes.c.id == id_docente)).first()

            if result:
                docente_dict = {
                    "id": result[0],
                    "contraseña": result[1],
                    "nombre": result[2],
                    "correo": result[3],
                    "campus": result[4],
                    "telefono": result[5],
                    "foto_perfil": result[6]
                }
                docente = Docente(**docente_dict)
                logging.info(
                    f"Se obtuvo información del docente con el ID: {id_docente}")
                return docente
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as exception_error:
        logging.error(
            f"Error al obtener información del docente con el ID : {id_docente} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.post("/docentes")
def create_docente(data_docente: Docente):
    try:
        with engine.connect() as conn:

            result = conn.execute(docentes.select().where(
                docentes.c.nombre == data_docente.nombre)).first()

            if result != None:
                return Response(status_code=HTTP_401_UNAUTHORIZED)

            new_docente = Docente
            new_docente.contraseña = generate_password_hash(data_docente.contraseña, "pbkdf2:sha256:30", 30)
            new_docente.nombre = data_docente.nombre

            result_create = conn.execute(docentes.insert().values(
                contraseña=new_docente.contraseña,
                nombre=new_docente.nombre
            ))
            conn.commit()
        return Response(status_code=HTTP_201_CREATED)
    except Exception as exception_error:
        return Response(status_code=SERVER_ERROR)
    except Exception as e:
        print("Error al insertar los datos en la base de datos:", e)
        return Response(content={"mensaje": "Los datos ingresados son incorrectos."}, status_code=HTTP_400_BAD_REQUEST)


@docenteRouter.post("/docente", status_code=HTTP_201_CREATED)
def docentes_ingresar_al_sistema(estudiantes_auth: EstudianteAuth):
    try:
        with engine.connect() as conn:
            if (estudiantes_auth.correo != None):
                result = conn.execute(estudiantes.select().where(
                    estudiantes.c.correo == estudiantes_auth.correo)).first()
            if (estudiantes_auth.matricula != None):
                result = conn.execute(estudiantes.select().where(
                    estudiantes.c.matricula == estudiantes_auth.matricula)).first()
            if result != None:
                check_passw = check_password_hash(result[2], estudiantes_auth.contraseña)
                if check_passw:
                    class_by_miuv = get_class_uv(user=estudiantes_auth.matricula, password=estudiantes_auth.contraseña)
                    class_dict = json.loads(class_by_miuv)
                    dic = class_dict['clases']
                    for clase, detalles in dic.items():
                        acad = detalles["general"].get("acad")
                        print(acad)
                        result = conn.execute(docentes.select().where(
                            docentes.c.nombre == acad)).first()
                        if (result == None):
                            new_docente = Docente
                            new_docente.nombre = acad
                            new_docente.contraseña = generate_password_hash("password", "pbkdf2:sha256:30", 30)

                            result_create = conn.execute(
                                docentes.insert().values(
                                    contraseña=new_docente.contraseña,
                                    nombre=new_docente.nombre
                                ))
                            conn.commit()
                            logging.info(
                                f"Docente {new_docente.nombre} creado correctamente")
                        nrc = clase

                        if (detalles["detalles"].get("nrc")) is not None:
                            nrc = detalles["detalles"]["nrc"]

                        result = conn.execute(docentes.select().where(
                            docentes.c.nombre == acad)).first()

                        id_docente = result.id
                        result = conn.execute(clases.select().where(
                            clases.c.nrc == nrc)).first()
                        id_clase = result.id
                        print(id_clase)
                        result = conn.execute(horarioDocentes.select().where(horarioDocentes.c.id_clase == id_clase)).first()
                        print(result)
                        if result is None:
                            print("guardara")
                            result = conn.execute(horarioDocentes.insert().values(
                                id_docente=id_docente,
                                id_clase=id_clase
                            ))
                            conn.commit()

                    return {
                        "status": 200,
                        "message": "Access success",
                        "token": write_token(estudiantes_auth.dict()),
                    }
                else:
                    return Response(status_code=HTTP_401_UNAUTHORIZED)

            else:
                return Response(status_code=HTTP_204_NO_CONTENT)

    except Exception as exception_error:
        logging.error(
            f"Error al ingresar docente al sistema ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)


@docenteRouter.put("/docente/{id_docente}", response_model=DocenteUpdate)
def update_docente(data_update: DocenteUpdate, id_docente: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(docentes.select().where(
                docentes.c.id == id_docente)).first()
            if result:
                encryp_passw = generate_password_hash(data_update.contraseña, "pbkdf2:sha256:30", 30)

                result = conn.execute(docentes.update().values(
                    contraseña=encryp_passw,
                    telefono=data_update.telefono,
                    correo=data_update.correo,
                    campus=data_update.campus,
                    foto_perfil=data_update.foto_perfil
                ).where(docentes.c.id == id_docente))

                conn.commit()
                result = conn.execute(docentes.select().where(
                    docentes.c.id == id_docente)).first()

                logging.info(
                    f"Docente con el ID: {id_docente} actualizado correctamente")

                return Response(status_code=HTTP_201_CREATED)
            else:
                return Response(status_code=HTTP_204_NO_CONTENT)

    except Exception as exception_error:
        logging.error(
            f"Error al actualizar el docente con el ID: {id_docente} ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)




@docenteRouter.post("/docente/login", status_code=HTTP_201_CREATED)
def docentes_ingresar_al_sistema(docentes_auth: DocenteAuth):
    try:
        with engine.connect() as conn:
            if (docentes_auth.correo != None):
                result = conn.execute(docentes.select().where(
                    docentes.c.correo == docentes_auth.correo)).first()
            if (docentes_auth.id != None):
                result = conn.execute(docentes.select().where(
                    docentes.c.id == docentes_auth.id)).first()

            print(result)

            if result != None:
                check_passw = check_password_hash(result[1], docentes_auth.contraseña)
                if check_passw:
                    print("entro")
                    return {
                        "status": 200,
                        "message": "Access success",
                        "token": write_token(docentes_auth.dict()),
                        "user": get_docente_by_id_docente(result[0])
                    }
                else:
                    return Response(status_code=HTTP_401_UNAUTHORIZED)

            else:
                return Response(status_code=HTTP_204_NO_CONTENT)

    except Exception as exception_error:
        logging.error(
            f"Error al ingresar docente al sistema ||| {exception_error}")
        return Response(status_code=SERVER_ERROR)



@docenteRouter.post("/docente/verify/token")
def docentes_verificar_token(token_docente: str = Header(default=None)):
    # token = user_token.split(' ')[1]
    token = token_docente.split(" ")[0]
    return validate_token(token_docente, output=True)
