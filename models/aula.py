from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


aulas = Table("aulas", meta_data,
              Column('id', Integer, primary_key=True),
              Column('nombre', String(200)),
              Column('id_edificio', Integer, ForeignKey(
                  'edificios.id')),

              )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
