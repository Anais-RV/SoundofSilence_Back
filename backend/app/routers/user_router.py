from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.app import database, models
from backend.app.schemas.user_schema import User, UserCreate
from ..database import get_db
import shutil

router = APIRouter()

@router.post("/register", response_model=User)
# def register_user(user: UserCreate, db: Session = Depends(get_db), profile_image: UploadFile = File(...)):
def register_user(
    user: UserCreate = Depends(),  # Esto cambió
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.user_name == user.user_name)).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    image_path = "images/" + profile_image.filename
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)

    new_user = models.User(
        name=user.name,
        last_name=user.last_name,
        user_name=user.user_name,
        email=user.email,
        profile_image=image_path  # ruta de la imagen
    )

    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# import shutil

# router = APIRouter()

# @router.post("/register", response_model=User)
# def register_user(user: UserCreate, profile_image: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         # Validar si el usuario ya existe
#         db_user = db.query(models.User).filter(
#             (models.User.email == user.email) | (models.User.user_name == user.user_name)).first()

#         if db_user:
#             raise HTTPException(status_code=400, detail="Username or Email already registered")

#         # Ruta de la imagen
#         image_path = "images/" + profile_image.filename
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(profile_image.file, buffer)

#         # Crear el nuevo usuario en la base de datos
#         new_user = models.User(
#             name=user.name,
#             last_name=user.last_name,
#             user_name=user.user_name,
#             email=user.email,
#             profile_image=image_path
#         )

#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)

#         return new_user

#     except Exception as e:
#         # Maneja cualquier excepción aquí
#         raise HTTPException(status_code=500, detail="Error during user registration")