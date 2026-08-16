
from database.connexion import ConnexionBD


def inserer_donnees_test():
    print("=" * 55)
    print("  SEEDER : INSERTION DU JEU DE DONNÉES DE TEST")
    print("=" * 55)

    conn = ConnexionBD.get_instance()
    if not conn:
        print("[ERREUR] Impossible de se connecter à la base de données.")
        return

    cursor = None
    try:
        cursor = conn.cursor()

        # 1. Insertion des utilisateurs de test
        utilisateurs = [
            (1, 'admin', 'admin123', 'DIOP', 'Amadou', 'admin@entreprise.sn', 'ADMIN', 'Direction'),
            (2, 'tech1', 'tech123', 'NDIAYE', 'Fatou', 'fatou.ndiaye@entreprise.sn', 'TECHNICIEN', 'Support Informatique'),
            (3, 'tech2', 'tech123', 'SOW', 'Moussa', 'moussa.sow@entreprise.sn', 'TECHNICIEN', 'Réseaux & Télécoms'),
            (4, 'user1', 'user123', 'FALL', 'Awa', 'awa.fall@entreprise.sn', 'UTILISATEUR', 'Comptabilité'),
            (5, 'user2', 'user123', 'BA', 'Ibrahima', 'ibrahima.ba@entreprise.sn', 'UTILISATEUR', 'Ressources Humaines')
        ]

        query_user = """
        INSERT INTO `utilisateur` (`id`, `login`, `password`, `nom`, `prenom`, `email`, `role`, `service`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE `nom`=VALUES(`nom`), `prenom`=VALUES(`prenom`);
        """
        cursor.executemany(query_user, utilisateurs)
        print(f"[OK] {len(utilisateurs)} utilisateurs insérés/mis à jour.")

        # 2. Insertion des incidents de test
        incidents = [
            (1, "Imprimante RH hors service", "L'imprimante réseau du bureau RH n'imprime plus les fiches de paie.", "HAUTE", "OUVERT", 5),
            (2, "Écran noir poste comptabilité", "Le PC de travail ne s'allume plus après la coupure de courant.", "CRITIQUE", "EN_COURS", 4),
            (3, "Lenteur connexion Wi-Fi", "Connexion très lente au 2ème étage lors des réunions.", "MOYENNE", "RESOLU", 5),
            (4, "Demande de souris sans fil", "Besoin d'une nouvelle souris ergonomique.", "BASSE", "FERME", 4)
        ]

        query_incident = """
        INSERT INTO `incident` (`id`, `titre`, `description`, `priorite`, `statut`, `utilisateur_id`)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE `titre`=VALUES(`titre`), `statut`=VALUES(`statut`);
        """
        cursor.executemany(query_incident, incidents)
        print(f"[OK] {len(incidents)} incidents insérés/mis à jour.")

        # 3. Insertion des interventions de test
        interventions = [
            (1, "Diagnostic en cours : test du bloc d'alimentation et barrettes RAM.", 45, 2, 2),
            (2, "Redémarrage et mise à jour logicielle du point d'accès Wi-Fi.", 30, 3, 3),
            (3, "Souris sans fil livrée et testée sur le poste de l'utilisateur.", 15, 4, 2)
        ]

        query_interv = """
        INSERT INTO `intervention` (`id`, `commentaire`, `duree_minutes`, `incident_id`, `technicien_id`)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE `commentaire`=VALUES(`commentaire`);
        """
        cursor.executemany(query_interv, interventions)
        print(f"[OK] {len(interventions)} interventions insérées/mises à jour.")

        conn.commit()
        print("-" * 55)
        print("Seeding terminé avec succès ! Les données de test sont disponibles.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERREUR] Échec du seeding : {e}")
    finally:
        if cursor is not None:
            cursor.close()


if __name__ == "__main__":
    inserer_donnees_test()
