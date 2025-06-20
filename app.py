from classes.reactor import Reactor
from classes.supervisor import Supervisor
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv("URI")

def get_collection(uri, db="planta_nuclear", coll="reactores"):
    client = MongoClient(uri, server_api=ServerApi("1"), tls=True, tlsAllowInvalidCertificates=True)
    client.admin.command("ping")
    return client[db][coll]

def main():
    coll_reactor = get_collection(URI, coll="reactores")
    coll_supervisor = get_collection(URI, coll="supervisores")

    # Paso 1: Crear y guardar un reactor
    reactor = Reactor("Reactor Omega", "Uranio_235", "LWR", 1200.0)
    reactor_id = reactor.save(coll_reactor)
    print(f"Reactor guardado con _id: {reactor_id}")

    # Paso 2: Crear supervisor y asignarlo al reactor
    supervisor = Supervisor("Dr. Emilio García", 45, "Ucraniana", "NR-001")
    reactor.assign_supervisor(supervisor)

    # Paso 3: Guardar el supervisor (incluye reactor._id)
    supervisor_id = supervisor.save(coll_supervisor)
    print(f"Supervisor guardado con _id: {supervisor_id}")

    # Paso 4: Actualizar el reactor con el supervisor._id
    result = reactor.update_supervisor(coll_reactor, supervisor_id)
    if result.modified_count > 0:
        print("Reactor actualizado con el supervisor_id correctamente.")
    else:
        print("No se pudo actualizar el reactor.")

if __name__ == "__main__":
    main()