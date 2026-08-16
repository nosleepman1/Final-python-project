from database.connexion import ConnexionBD


class StatistiqueDAO:

    def __init__(self):
        self.conn = ConnexionBD.get_instance()

    def incidents_par_statut(self):
        if not self.conn:
            return []
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = "SELECT statut, COUNT(*) AS total FROM incident GROUP BY statut"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def incidents_par_priorite(self):
        if not self.conn:
            return []
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = "SELECT priorite, COUNT(*) AS total FROM incident GROUP BY priorite"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def top_techniciens(self):
        if not self.conn:
            return []
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = """
            SELECT u.nom, u.prenom, COUNT(*) AS nb_interventions
            FROM intervention i
            JOIN utilisateur u ON u.id = i.technicien_id
            GROUP BY u.id, u.nom, u.prenom
            ORDER BY nb_interventions DESC
            LIMIT 3
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def temps_moyen_resolution(self):
        if not self.conn:
            return {"moyenne_heures": 0}
        cursor = self.conn.cursor(dictionary=True)
        try:
            query = "SELECT IFNULL(AVG(duree_minutes)/60, 0) AS moyenne_heures FROM intervention"
            cursor.execute(query)
            return cursor.fetchone()
        finally:
            cursor.close()