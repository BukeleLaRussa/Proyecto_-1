from typing import TYPE_CHECKING, Optional
from bson import ObjectId

if TYPE_CHECKING:
    from .reactor import Reactor

class Supervisor:
    def __init__(self, nombre: str, edad: int, nacionalidad: str, certificado: str):
        self.nombre = nombre
        self.edad = edad
        self.nacionalidad = nacionalidad
        self.certificado = certificado
        self.reactor: Optional["Reactor"] = None
        self._id: Optional[ObjectId] = None

    def save(self, coll):
        data = {
            "nombre": self.nombre,
            "edad": self.edad,
            "nacionalidad": self.nacionalidad,
            "certificado": self.certificado,
            "reactor_id": self.reactor._id if self.reactor else None
        }
        result = coll.insert_one(data)
        self._id = result.inserted_id
        return str(self._id)

    def __str__(self):
        return f"Supervisor - Nombre: {self.nombre}, Edad: {self.edad}, Nacionalidad: {self.nacionalidad}, Certificado: {self.certificado}"