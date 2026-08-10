# dao/base_dao.py
from abc import ABC, abstractmethod
from database.connexion import ConnexionBD

class BaseDAO(ABC):
    def __init__(self):
        self.conn = ConnexionBD.get_instance()

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def delete_by_id(self, id):
        pass