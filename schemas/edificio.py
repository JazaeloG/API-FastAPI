
from pydantic import BaseModel, EmailStr
from typing import Optional


class Edificio(BaseModel):
    id: Optional[int]
    nombre: str
    facultad: Optional[str]
    campus: Optional[str]