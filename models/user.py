from sqlalchemy import Table, Column, Integer, CHAR, VARCHAR, Text, DateTime
from config.db import meta_data, engine


users = Table("users", meta_data,
              Column("matricula", CHAR(10), primary_key=True),
              Column("contraseña", VARCHAR(40), nullable=False),
              Column("nombre", VARCHAR(200), nullable=False),
              Column("telefono", Integer(10), nullable=False),
              Column("correo", CHAR(18), nullable=False),
              Column("campus", VARCHAR(50), nullable=False),
              Column("semestre", Integer, nulleable=False),
              Column("periodo", VARCHAR(50), nulleable=False),


              Column('foto_perfil', Text),

              Column('fecha_de_creacion', DateTime(), default=datetime.now()),
              )

meta_data.bind = engine
meta_data.create_all()
