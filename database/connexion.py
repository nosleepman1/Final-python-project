# database/connexion.py
import mysql.connector
from mysql.connector import Error
from database.config import DB_CONFIG

class ConnexionBD:
    __instance = None

    @staticmethod
    def get_instance():
        if ConnexionBD.__instance is None or not ConnexionBD.__instance.is_connected():
            ConnexionBD()
        return ConnexionBD.__instance

    def __init__(self):
        if ConnexionBD.__instance is not None and ConnexionBD.__instance.is_connected():
            raise Exception("Cette classe est un Singleton. Utilisez ConnexionBD.get_instance().")
        else:
            try:
                self.connexion = mysql.connector.connect(**DB_CONFIG)
                ConnexionBD.__instance = self.connexion
            except Error as e:
                print(f"Erreur de connexion à MySQL : {e}")
                ConnexionBD.__instance = None