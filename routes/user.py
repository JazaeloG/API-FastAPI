from fastapi import APIRouter
from config.db import conn
from models.user import estudiantes
from schemas.user import Estudiante

estudiante = APIRouter()

@estudiante.get("/estudiantes")
def get_uestudiantes():
    return conn.execute(estudiantes.select()).fetchall()


@estudiante.post("/estudiantes")
def create_uestudiante(estudiante: Estudiante):
    new_estudiante = {
        "matricula":estudiante.matricula,
        "contraseña":estudiante.contraseña,
        "nombre":estudiante.nombre,
        "correo":estudiante.correo,
        "semestre":estudiante.semestre,
        "campus":estudiante.campus,
        "telefono":estudiante.telefono,
        "foto_perfil":estudiante.foto_perfil
    }
    print(new_estudiante)
    result = conn.execute(estudiantes.insert().values(new_estudiante))
    print(result.lastrowid)

    return conn.execute(estudiantes.select().where(estudiantes.c.id == result.lastrowid)).first()