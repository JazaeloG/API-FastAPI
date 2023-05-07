
from pydantic import BaseModel, EmailStr
from typing import Optional

class HorarioAula(BaseModel):
    id: int
    id_aula: int
    id_clase: int