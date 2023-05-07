from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


edificios  = Table("edificios", meta_data,
                  Column('id', Integer, primary_key=True),
                  Column('nombre', String(200), nullable=False),
                  Column('facultad', String(200)),
                  Column("campus", String(200)),
                  )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
