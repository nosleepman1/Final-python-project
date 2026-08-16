
import mysql.connector
from database.config import DB_CONFIG


def creer_tables():
    print("=" * 55)
    print("  MIGRATION : CRÉATION DE LA BASE ET DES TABLES")
    print("=" * 55)

    # 1. Connexion au serveur MySQL sans spécifier la base (pour pouvoir la créer)
    config_server = DB_CONFIG.copy()
    db_name = config_server.pop('database', 'gestion_incidents')
    config_server['use_pure'] = True

    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**config_server)
        cursor = conn.cursor()

        # Création de la base de données si elle n'existe pas
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE `{db_name}`")
        print(f"[OK] Base de données '{db_name}' vérifiée / créée.")

        # 2. Création des tables dans l'ordre (en respectant les clés étrangères)
        # Table utilisateur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `utilisateur` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `login` VARCHAR(50) NOT NULL UNIQUE,
            `password` VARCHAR(100) NOT NULL,
            `nom` VARCHAR(50) NOT NULL,
            `prenom` VARCHAR(50) NOT NULL,
            `email` VARCHAR(100) NOT NULL,
            `role` ENUM('UTILISATEUR', 'TECHNICIEN', 'ADMIN') NOT NULL DEFAULT 'UTILISATEUR',
            `service` VARCHAR(50) DEFAULT NULL,
            `date_creation` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        """)
        print("[OK] Table 'utilisateur' créée avec succès.")

        # Table incident
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `incident` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `titre` VARCHAR(150) NOT NULL,
            `description` TEXT NOT NULL,
            `priorite` ENUM('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE') NOT NULL DEFAULT 'MOYENNE',
            `statut` ENUM('OUVERT', 'EN_COURS', 'RESOLU', 'FERME', 'ANNULE') NOT NULL DEFAULT 'OUVERT',
            `date_creation` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `utilisateur_id` INT NOT NULL,
            CONSTRAINT `fk_incident_utilisateur` 
                FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur`(`id`) 
                ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """)
        print("[OK] Table 'incident' créée avec succès.")

        # Table intervention
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `intervention` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `commentaire` TEXT NOT NULL,
            `duree_minutes` INT NOT NULL DEFAULT 0,
            `date_intervention` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `incident_id` INT NOT NULL,
            `technicien_id` INT NOT NULL,
            CONSTRAINT `fk_intervention_incident` 
                FOREIGN KEY (`incident_id`) REFERENCES `incident`(`id`) 
                ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT `fk_intervention_technicien` 
                FOREIGN KEY (`technicien_id`) REFERENCES `utilisateur`(`id`) 
                ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """)
        print("[OK] Table 'intervention' créée avec succès.")

        conn.commit()
        print("-" * 55)
        print("Migration terminée avec succès ! Toutes les tables sont prêtes.")

    except Exception as e:
        print(f"[ERREUR] Échec de la création des tables : {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    creer_tables()
