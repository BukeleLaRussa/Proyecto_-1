from typing import TYPE_CHECKING, Optional
from pymongo.collection import Collection
from bson import ObjectId

if TYPE_CHECKING:
    from .supervisor import Supervisor

class Reactor:
    def __init__(self, nombre: str, combustible: str, tipo: str, potencia_mw: float):
        self.nombre = nombre
        self.combustible = combustible
        self.tipo = tipo
        self.potencia_mw = potencia_mw
        self.supervisor: Optional["Supervisor"] = None
        self._id: Optional[ObjectId] = None

    def assign_supervisor(self, supervisor: Optional["Supervisor"]):
        if supervisor is None:
            print("Se requiere un supervisor válido.")
        else:
            self.supervisor = supervisor
            supervisor.reactor = self

    def save(self, coll):
        data = {
            "nombre": self.nombre,
            "combustible": self.combustible,
            "tipo": self.tipo,
            "potencia_mw": self.potencia_mw,
            "supervisor_id": self.supervisor._id if self.supervisor else None
        }
        result = coll.insert_one(data)
        self._id = result.inserted_id
        return str(self._id)

    def update_supervisor(self, coll: Collection, supervisor_id: str):
        if not self._id:
            raise ValueError("Reactor debe guardarse antes de actualizarse.")

        filtro = {"_id": ObjectId(self._id)}
        nuevos_valores = {"$set": {"supervisor_id": ObjectId(supervisor_id)}}
        result = coll.update_one(filtro, nuevos_valores)
        if result.matched_count == 0:
            print("No se encontró ningún reactor con ese _id para actualizar.")
        elif result.modified_count == 0:
            print("El campo supervisor_id ya tenía ese valor, no se modificó.")
            
        return result

    def __str__(self):
        return f"Reactor - Nombre: {self.nombre}, Combustible: {self.combustible}, Tipo: {self.tipo}, Potencia: {self.potencia_mw} MW"