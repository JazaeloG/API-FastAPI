from fastapi import FastAPI
from routes.estudiante import estudianteRouter

app = FastAPI()

app.include_router(estudianteRouter)