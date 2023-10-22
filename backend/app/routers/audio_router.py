from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from .. import database, models, schemas
from backend.app.schemas.audio_schema import Audio, AudioCreate
from backend.app.schemas.prediction_schema import Prediction
from fastapi import UploadFile, File, Form
from datetime import datetime
from typing import Optional, List
from ..models import audio_model
import base64, io, shutil, os
from fastapi.responses import StreamingResponse
from ..aiModels.sound_model import classify_sound
from  ..models import prediction_model  
from ..models.user_model import User as UserModel
from .user_router import get_current_user_id




router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# USER_ID_STATIC = 1  # ID del usuario tester

import subprocess

def process_audio(input_path: str, output_path: str):
    # Convierte el audio a 16kHz, mono, formato WAV
    command = [
        "ffmpeg", 
        "-i", input_path,
        "-ar", "16000",      # Frecuencia de muestreo a 16kHz
        "-ac", "1",          # Mono
        "-acodec", "pcm_s16le",  # Codificación de audio
        "-f", "wav",         # Formato de salida WAV
        output_path
    ]
    subprocess.run(command, check=True)



# GENERAR LAS PREDICCIONES DE UN AUDIO + GENERAR REGISTROS EN AUDIO & PREDICCIONES
@router.post("/audios", response_model=Audio)

def create_audio(user_id: int = Depends(get_current_user_id), blob_data: UploadFile = File(...), path: Optional[str] = Form(None), db: Session = Depends(get_db)):    
    
    # Nombre temporal para el archivo procesado
    processed_filename = "processed_" + blob_data.filename
    
    # Guarda el archivo en el servidor 
    with open(blob_data.filename, "wb") as buffer:
        shutil.copyfileobj(blob_data.file, buffer)
    
    # Procesa el audio
    process_audio(blob_data.filename, processed_filename)
    
    # Abre el archivo procesado y lee el contenido para codificarlo
    with open(processed_filename, "rb") as buffer:
        file_content = buffer.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
    
    # Convierte el contenido codificado en bytes antes de insertarlo
    db_audio = audio_model.Audio(blob_data=encoded_content.encode("utf-8"), path=path, timestamp=datetime.now())
    
    # Agrega el audio y confirma para obtener el ID del audio
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    
    # Procesar audio con YAMNet
    try:
        labels, scores = classify_sound(processed_filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {e}")
    
    # Agrega las predicciones con el audio_id
    for label, score in zip(labels, scores):
        prediction = prediction_model.Prediction(label=label, confidence=score, audio_id=db_audio.id, user_id=user_id)
        db.add(prediction)
    db.commit()  # Commit the predictions

    # Limpia los archivos temporales
    os.remove(blob_data.filename)
    os.remove(processed_filename)

    return db_audio



# RECUPERAR UN AUDIO EN STREAMING
@router.get("/audios/{audio_id}")
async def get_audio(audio_id: int, db: Session = Depends(get_db)):
    db_audio = db.query(audio_model.Audio).filter(audio_model.Audio.id == audio_id).first()
    if not db_audio:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    # Decodificar el contenido de Base64 a bytes
    decoded_content = base64.b64decode(db_audio.blob_data)

    # Convertir los bytes decodificados en un objeto BytesIO
    audio_stream = io.BytesIO(decoded_content)

    # Crear y devolver una respuesta en streaming
    return StreamingResponse(audio_stream, media_type="audio/wav")


# OBTENER TODAS LAS PREDICCIONES DE UN AUDIO
@router.get("/audios/{audio_id}/predictions", response_model=List[Prediction])
def get_predictions_for_audio(audio_id: int, db:Session = Depends(get_db)):
    print(f"Fetching predictions for audio ID: {audio_id}")  # Esto imprimirá el ID del audio que estamos buscando
    predictions = db.query(prediction_model.Prediction).filter(prediction_model.Prediction.audio_id == audio_id).all()

    print(f"Found {len(predictions)} predictions")  # Esto imprimirá la cantidad de predicciones encontradas

    if not predictions:
        raise HTTPException(status_code=404, detail="Predictions not found for this audio")
    
    return predictions


# HISTORIAL
@router.get("/user/{user_id}/last_audios", response_model=List[Prediction])
def get_last_audios_for_users(user_id: int, db: Session = Depends(get_db)):
    subquery = (
        db.query(prediction_model.Prediction.audio_id)
        .filter(prediction_model.Prediction.user_id == user_id)
        .distinct()
        .order_by(desc(prediction_model.Prediction.timestamp))
        .limit(5)
        .subquery()
    )

    last_audios = (
        db.query(prediction_model.Prediction)
        .filter(prediction_model.Prediction.audio_id.in_(subquery))
        .order_by(asc(prediction_model.Prediction.timestamp))
        .all()
    )

    if not last_audios:
        raise HTTPException(status_code=404, detail="No audios found for this user")

    return last_audios

# ELIMINAR UN AUDIO
@router.delete("/audios/{audio_id}", response_model=Audio)

def delete_audio(audio_id: int, db: Session = Depends(get_db)):

    db_audio = db.query(audio_model.Audio).filter(audio_model.Audio.id == audio_id).first()
    if not db_audio:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    #antes de eliminar el audio, eliminamos predicciones asociadas (privacidad usuario)

    db.query(prediction_model.Prediction).filter(prediction_model.Prediction.audio_id == audio_id).delete()
    
    db.delete(db_audio)
    db.commit()

    return db_audio

