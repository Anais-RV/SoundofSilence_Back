from pydantic import BaseModel

class PredictionBase(BaseModel):
    id: int
    label: str
    confidence: float
    audio_id: int
    user_id: int

class PredictionCreate(PredictionBase):
    pass 

class Prediction(PredictionBase):

    class Config:
        from_attributes = True