from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AudioBase(BaseModel):  #objeto base
    blob_data: bytes
    path: Optional[str]
    timestamp: datetime

class AudioCreate(AudioBase): #extensión del objeto, lo usaremos para crear un audio, solo necesita el schema base
    pass

class Audio(AudioBase): #extensión del objeto, lo utilizaremos para devolver detalles de un audio por ejemplo
    id: int

    class Config: #clase interna de pydantic - facilita la conversión de un objeto ORM a une esquema
        from_attributes = True

