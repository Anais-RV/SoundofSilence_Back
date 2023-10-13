from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from ..database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    confidence = Column(Float)  
    timestamp = Column(DateTime(timezone=True), default=func.now())
    
    user_id = Column(Integer, ForeignKey('users.id'))
    audio_id = Column(Integer, ForeignKey('audios.id'))

    user = relationship("User", back_populates="predictions")
    audio = relationship("Audio", back_populates="predictions")
    feedback = relationship("Feedback", back_populates="prediction", uselist=False)
