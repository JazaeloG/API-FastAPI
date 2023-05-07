from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


horarioAulas = Table("horarioAulas", meta_data,
                           Column('id', Integer, primary_key=True),
                           Column('id_aula', Integer, ForeignKey(
                               "aulas.id")),
                           Column('id_clase', Integer, ForeignKey(
                               "clases.id"))
                           )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
