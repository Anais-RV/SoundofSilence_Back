from sqlalchemy import Column, Boolean, String, ForeignKey, Integer
from ..database import Base
from sqlalchemy.orm import relationship

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    is_correct = Column(Boolean, nullable=True)
    comment = Column(String, nullable=True)

    prediction_id = Column(Integer, ForeignKey('predictions.id'))

    prediction = relationship("Prediction", back_populates="feedback")
    