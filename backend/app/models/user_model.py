from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, validates
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_image = Column(String, nullable=True)
    
    @validates('email')
    def validate_email(self, key, email):
        if not EMAIL_REGEX.match(email):
            raise ValueError("Provided email is not in a valid format")
        return email

    hashed_password = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    predictions = relationship("Prediction", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

