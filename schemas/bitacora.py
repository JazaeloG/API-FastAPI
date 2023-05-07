
from pydantic import BaseModel, EmailStr
from typing import Optional

class Bitacora(BaseModel):
    id: Optional[int]
    id_clase: int
    id_estudiante: Optional[int]
    id_docente: Optional[int]
    id_aula: int
    tipo: str
    hora: str