from classes.reactor import Reactor
from classes.supervisor import Supervisor
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import unittest
import os

load_dotenv()
URI = os.getenv("URI")

class TestRelacionUnoAUno(unittest.TestCase):
    def setUp(self):
        # Crear el cliente y colecciones
        self.client = MongoClient(URI, tls=True, tlsAllowInvalidCertificates=True)
        db = self.client["planta_nuclear"]
        self.coll_reactor = db["reactores_test"]
        self.coll_supervisor = db["supervisores_test"]

    def tearDown(self):
        # Cerrar el cliente después de cada prueba
        self.client.close()

    def test_1_guardado_supervisor_con_id_de_reactor(self):
        reactor = Reactor("Reactor Prueba", "Uranio", "BWR", 1000.0)
        reactor_id = reactor.save(self.coll_reactor)

        supervisor = Supervisor("Ana Torres", 42, "Argentina", "NR-002")
        reactor.assign_supervisor(supervisor)
        supervisor_id = supervisor.save(self.coll_supervisor)

        doc = self.coll_supervisor.find_one({"_id": ObjectId(supervisor_id)})
        self.assertIsNotNone(doc)
        self.assertEqual(str(doc["reactor_id"]), str(reactor._id))

    def test_2_actualizacion_reactor_con_id_de_supervisor(self):
        reactor = Reactor("Reactor Prueba", "Uranio", "BWR", 1000.0)
        reactor_id = reactor.save(self.coll_reactor)

        supervisor = Supervisor("Ana Torres", 42, "Argentina", "NR-002")
        reactor.assign_supervisor(supervisor)
        supervisor_id = supervisor.save(self.coll_supervisor)

        result = reactor.update_supervisor(self.coll_reactor, supervisor_id)
        self.assertGreaterEqual(result.matched_count, 1)

        updated_doc = self.coll_reactor.find_one({"_id": ObjectId(reactor_id)})
        self.assertIsNotNone(updated_doc)
        self.assertEqual(str(updated_doc["supervisor_id"]), str(supervisor._id))

if __name__ == "__main__":
    unittest.main()