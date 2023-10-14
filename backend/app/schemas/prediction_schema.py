from pydantic import BaseModel

class PredictionBase(BaseModel):
    label: str
    confidence: float
    audio_id: int
    user_id: int

class PredictionCreate(PredictionBase):
    pass 

class Prediction(BaseModel):
    id: int

    class Config:
        orm_mode = True