
from pydantic import BaseModel, EmailStr
from typing import Optional

class HorarioDocente(BaseModel):
    id: int
    id_docente: str
    id_clase: int