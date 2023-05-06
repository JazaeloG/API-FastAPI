from datetime import datetime 
from sqlalchemy import Table, Column, Integer,String, Text, DateTime
from config.db import meta_data, engine 



clases = Table("clases", meta_data,
    Column('id', Integer, primary_key=True),
    Column("nrc", String(200), nullable=False),
    Column("nombre", String(200), nullable=False),
    Column("academico", String(200), nullable=False),
    Column("facultad", String(200), nullable=False),
    Column("campus", String(200)),
    Column('edificio', String(150), nullable=False),
    Column("aula", String(15), nullable=False),
    Column("lunes", String(15)),
    Column("martes", String(15)),
    Column("miercoles", String(15)),
    Column("jueves", String(15)),
    Column("viernes", String(15)),
    Column("sabado", String(15)),
)
meta_data.bind = engine
meta_data.create_all(meta_data.bind)
