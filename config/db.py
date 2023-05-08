from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()

# Se lee el archivo de configuración 
db_user = os.getenv('DEV_DB_USER')
db_password = os.getenv('DEV_DB_PASSWORD')
db_host = os.getenv('DEV_DB_HOST')
db_port = os.getenv('DEV_DB_PORT')
db_name = os.getenv('DEV_DB_NAME')


engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
#engine = create_engine(f'mysql+pymysql://root:password@localhost:3306/prueba')



conn = engine.connect()
meta_data = MetaData()