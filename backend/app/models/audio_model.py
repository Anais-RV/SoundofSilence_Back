from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, func
from ..database import Base
from sqlalchemy.orm import relationship

class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    blob_data = Column(LargeBinary) #datos binarios - permite guardar audio en bbdd
    path = Column(String, nullable=True) #no obligatorio pero sí contemplado para implementar almacenamiento cloud
    timestamp = Column (DateTime(timezone=True), default=func.now) #fecha automatica de creación del registro

    predictions = relationship("Prediction", back_populates="audio") #relación
