from fastapi import FastAPI
from backend.app.routers import audio_router
from backend.app.routers import user_router
from .models import audio_model, prediction_model, user_model, feedback_model


app = FastAPI()

@app.get("/")
def read_root():
    return{"HAPOLLO":"&COMPANY"}

app.include_router(audio_router.router, tags=["audios"])
app.include_router(user_router.router)