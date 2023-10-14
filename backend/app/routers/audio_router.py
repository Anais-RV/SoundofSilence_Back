from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas
from backend.app.schemas.audio_schema import Audio, AudioCreate
from fastapi import UploadFile, File, Form
from datetime import datetime
from typing import Optional
from ..models import audio_model
import base64, io, shutil
from fastapi.responses import StreamingResponse


router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/audios", response_model=Audio)
def create_audio(blob_data: UploadFile = File(...), path: Optional[str] = Form(None), db: Session = Depends(get_db)):
    
    # Guarda el archivo en el servidor 
    with open(blob_data.filename, "wb") as buffer:
        shutil.copyfileobj(blob_data.file, buffer)
    
    # Abre el archivo y lee el contenido para codificarlo
    with open(blob_data.filename, "rb") as buffer:
        file_content = buffer.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
    
    # Convierte el contenido codificado en bytes antes de insertarlo
    db_audio = audio_model.Audio(blob_data=encoded_content.encode("utf-8"), path=path, timestamp=datetime.now())
    
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    
    return db_audio


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


@router.delete("/audios/{audio_id}", response_model=Audio)

def delete_audio(audio_id: int, db: Session = Depends(get_db)):

    db_audio = db.query(audio_model.Audio).filter(audio_model.Audio.id == audio_id).first()


    if not db_audio:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    db.delete(db_audio)
    db.commit()
    return db_audio