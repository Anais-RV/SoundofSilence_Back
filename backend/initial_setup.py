from app.models import user_model, audio_model, prediction_model, feedback_model
from app.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine) #creamos todas las tablas definidas en los modelos gracias a SQLAlchemy 
    print("Tablas creadas!")

if __name__ == "__main__": #el código solo se ejecuta cuando se ejecuta el script 
    init_db()