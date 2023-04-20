from datetime import datetime 
from sqlalchemy import Table, Column, Integer,String, Text, DateTime
from config.db import meta_data, engine 


"""
    - Tienes dos veces la tabla telefono
    - En el schema tienes telefono como optional y aqui como no null
        asi que lo cambie a que puede ser null para que pueda ser opcional
"""

estudiantes = Table("estudiantes", meta_data,
    Column('id', Integer, primary_key=True),
    Column("matricula", String(10), nullable=False),
    Column("contraseña", String(40), nullable=False),
    Column("nombre", String(200), nullable=False),
    Column('correo', String(150), nullable=False),
    Column("campus", String(50), nullable=False),
    Column("semestre", Integer, nullable=False),
    Column("telefono", String(15)),
    #Column("telefono", String(15), nullable=False)
    Column('foto_perfil', Text),
    Column('fecha_de_creacion',DateTime(), default = datetime.now()),
)

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
