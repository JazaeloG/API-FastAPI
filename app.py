from fastapi import FastAPI
from routes.user import estudiante

app = FastAPI()

app.include_router(estudiante)