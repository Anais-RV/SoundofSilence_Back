from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from backend.app.routers import audio_router
from backend.app.routers import user_router
from .models import audio_model, prediction_model, user_model, feedback_model
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/images", StaticFiles(directory="D:/BOOTCAMPF5/SoundOfSilence/images"), name="images")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return{"HAPOLLO":"&COMPANY"}

app.include_router(audio_router.router, tags=["audios"])
app.include_router(user_router.router)