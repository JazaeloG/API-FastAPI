
from pydantic import BaseModel, EmailStr
from typing import Optional

class Bitacora(BaseModel):
    id: Optional[int]
    id_clase: int
    id_estudiante: int
    id_docente: int
    edificio: str
    aula: str
    tipo: str
    hora: str