from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


horarioEstudiantes = Table("horarioEstudiantes", meta_data,
                           Column('id', Integer, primary_key=True),
                           Column('id_estudiante', Integer, ForeignKey(
                               "estudiantes.id")),
                           Column('id_clase', Integer, ForeignKey(
                               "clases.id"))
                           )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)

""",
                            Column("academico", String(200)),
                            Column("lunes", String(200)),
                            Column("martes", String(200)),
                            Column("miercoles", String(200)),
                            Column("jueves", String(200)),
                            Column("viernes", String(200)),
                            Column("sabado", String(200)),
                            Column("edificio", String(200)),
                            Column("aula", String(50))"""
