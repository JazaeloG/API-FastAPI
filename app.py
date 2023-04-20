from fastapi import FastAPI
from routes.estudiante import estudianteRouter
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="REST API to Automation Documents by UV",
    description="By ISW UV",
    version="0.1",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudianteRouter)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
    #uvicorn.run(app, port=8080, host="127.0.0.1")