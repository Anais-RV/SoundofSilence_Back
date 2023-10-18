from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///backend/app/database/soundofsilence.db?check_same_thread=False" 
DATABASE_URL = "sqlite:///D:/BOOTCAMPF5/SoundOfSilence/backend/app/database/soundofsilence.db?check_same_thread=False"
 #cadena de conexión

engine = create_engine(DATABASE_URL) # conexión a la bbdd
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #"fabrica sesiones de bbdd, instancia en cada conexión, se cierra al terminar de operar"

Base = declarative_base() #clase base para definir los modelos de datos


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
