
from pydantic import BaseModel, EmailStr
from typing import Optional

class HorarioEstudiante(BaseModel):
    id: int
    id_estudiante: int
    clase_id: int
"""
class HorarioEstudianteGet(BaseModel):
    nombre: Optional[str] 
    academico: Optional[str] 
    lunes: Optional[str] 
    martes: Optional[str] 
    miercoles: Optional[str] 
    jueves: Optional[str] 
    viernes: Optional[str] 
    sabado: Optional[str] 
    edificio: Optional[str] 
    aula: Optional[str] """