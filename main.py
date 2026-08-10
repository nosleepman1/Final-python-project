# main.py
import time
import mysql.connector
from database.config import DB_CONFIG
from dao.utilisateur_dao import UtilisateurDAO
from models.utilisateur import Utilisateur


def initialiser_base_de_donnees():
    """Crée la base de données et la table utilisateur si elles n'existent pas encore."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG.get('host', '127.0.0.1'),
            user=DB_CONFIG.get('user', 'root'),
            password=DB_CONFIG.get('password', ''),
            port=DB_CONFIG.get('port', 3306)
        )
        cursor = conn.cursor()
        db_name = DB_CONFIG.get('database', 'gestion_incidents')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{db_name}`;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            login VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            nom VARCHAR(100) NOT NULL,
            prenom VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            role ENUM('UTILISATEUR', 'TECHNICIEN', 'ADMIN') NOT NULL DEFAULT 'UTILISATEUR',
            service VARCHAR(100) NOT NULL,
            date_creation DATE DEFAULT (CURRENT_DATE)
        ) ENGINE=InnoDB;
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Avertissement lors de la vérification de la base : {e}")


def test_crud_utilisateur():
    initialiser_base_de_donnees()
    dao = UtilisateurDAO()

    # Génération d'un login unique pour chaque exécution de test
    timestamp = int(time.time())
    login_test = f"user_{timestamp}"

    print("--- 1. Test d'ajout d'un utilisateur ---")
    nouveau_user = Utilisateur(
        login=login_test,
        password="pass123",
        nom="TINE",
        prenom="Mohamed",
        email=f"{login_test}@entreprise.sn",
        role="UTILISATEUR",
        service="Comptabilité"
    )

    user_cree = dao.add(nouveau_user)
    if user_cree:
        print(f"✅ Utilisateur créé avec succès ! ID: {user_cree.id} (Login: {user_cree.login})")
    else:
        print(" Échec de la création.")

    print("\n--- 2. Liste de tous les utilisateurs ---")
    utilisateurs = dao.get_all()
    for u in utilisateurs:
        print(f"- [{u.role}] {u.prenom} {u.nom} (@{u.login}) - Service: {u.service}")


if __name__ == "__main__":
    test_crud_utilisateur()