from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


bitacoras = Table("bitacoras", meta_data,
                  Column('id', Integer, primary_key=True),
                  Column('id_clase', Integer, ForeignKey(
                               "clases.id")),
                  Column('id_estudiante', Integer, ForeignKey(
                               "estudiantes.id")),
                  Column('id_docente', Integer, ForeignKey(
                      "docentes.id")),
                  Column('edificio',String(200), ForeignKey(
                    "clases.edificio")),
                
                  Column('aula', String(200), ForeignKey(
                    "clases.aula")),
                  Column('tipo', String(2)),
                  Column('hora', DateTime)
                  )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
