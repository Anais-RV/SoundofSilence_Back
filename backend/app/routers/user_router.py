from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user_model import User as UserModel
from ..schemas.user_schema import User, UserCreate, UserLogin, UserResponse
from werkzeug.security import check_password_hash
from fastapi import Form
from datetime import datetime, timedelta
import shutil, json, jwt

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(
    user: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_data = json.loads(user)  # Cambiar a json.loads

    db_user = db.query(UserModel).filter(
        (UserModel.email == user_data['email']) | (UserModel.user_name == user_data['user_name'])).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    # Guardar la imagen
    image_path = "images/" + profile_image.filename
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)

    # nuevo usuario
    new_user = UserModel(
        name=user_data['name'],
        last_name=user_data['last_name'],
        user_name=user_data['user_name'],
        email=user_data['email'],
        profile_image=image_path
    )
    new_user.set_password(user_data['password'])
    
    # Añadir el usuario a la bbdd
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.user_name == user.user_name).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not check_password_hash(db_user.hashed_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    return{"token": token, "user": db_user}