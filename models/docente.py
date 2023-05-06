from datetime import datetime 
from sqlalchemy import Table, Column, Integer,String, Text, DateTime
from config.db import meta_data, engine 



docentes = Table("docentes", meta_data,
    Column('id', Integer, primary_key=True),
    Column("contraseña", String(200), nullable=False),
    Column("nombre", String(200), nullable=False),
    Column('correo', String(150)),
    Column("campus", String(50)),
    Column("telefono", String(15)),
    Column('foto_perfil', Text)
)

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
