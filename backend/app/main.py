from fastapi import FastAPI
from backend.app.routers import audio_router
from .models import audio_model, prediction_model, user_model, feedback_model


app = FastAPI()

@app.get("/")
def read_root():
    return{"HAPOLLO":"SRA.SENIL"}

app.include_router(audio_router.router, tags=["audios"])