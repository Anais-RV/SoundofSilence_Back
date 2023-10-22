# Bibliotecas estándar
from datetime import datetime, timedelta
import json
import shutil

# Bibliotecas de terceros
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from fastapi.security import OAuth2PasswordBearer


# Importaciones específicas del módulo o aplicativo
from ..database import get_db
from ..models.user_model import User as UserModel
from ..schemas.user_schema import User, UserCreate, UserLogin, UserResponse


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
    
    access_token = create_access_token(data={"sub": user.user_name})
    
    # Devuelve todos los campos que UserResponse espera
    return {
        "token": access_token, 
        "user": {
            "id": db_user.id,
            "user_name": db_user.user_name,
            "name": db_user.name,
            "last_name": db_user.last_name,
            "profile_image": db_user.profile_image,
            "email": db_user.email  # Y cualquier otro campo que sea necesario
        }
    }



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise HTTPException(status_code=400, detail="Token is invalid")
        return user_name
    except JWTError:
        raise HTTPException(status_code=400, detail="Token is invalid")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_name = verify_token(token)
    db_user = db.query(UserModel).filter(UserModel.user_name == user_name).first()
    if db_user:
        return db_user.id
    else:
        raise HTTPException(status_code=404, detail="User not found")