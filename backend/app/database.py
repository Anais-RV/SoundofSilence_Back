from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeBase, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app/database/soundofsilence.db"  #cadena de conexión

engine = create_engine(DATABASE_URL) # conexión a la bbdd
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) #"fabrica sesiones de bbdd, instancia en cada conexión, se cierra al terminar de operar"

Base = declarative_base() #clase base para definir los modelos de datos