
from pydantic import BaseModel, EmailStr
from typing import Optional

class Docente(BaseModel):
    id: Optional[int]
    contraseña: str
    nombre: str
    contraseña: Optional[str]
    telefono: Optional[str]
    correo: Optional[EmailStr]  
    campus: Optional[str]
    foto_perfil: Optional[str]

class DocenteUpdate(BaseModel):
    contraseña: Optional[str]
    telefono: Optional[str]
    correo: Optional[EmailStr]  
    campus: Optional[str]
    foto_perfil: Optional[str]
    
class DocenteAuth(BaseModel):
    id: Optional[str]
    correo : Optional[EmailStr]
    contraseña: str