
from pydantic import BaseModel, EmailStr
from typing import Optional

class Estudiante(BaseModel):
    id: Optional[int]
    matricula: str
    contraseña: str
    nombre: str
    correo: EmailStr    
    campus: str
    semestre: int
    telefono: Optional[str]
    foto_perfil: Optional[str]

class EstudianteSettings(BaseModel):
    contrasena: str
    telefono: str
    foto_perfil: Optional[str]
    
class EstudianteAuth(BaseModel):
    matricula: Optional[str]
    correo : Optional[EmailStr]
    contraseña: str