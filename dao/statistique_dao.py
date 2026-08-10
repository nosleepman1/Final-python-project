from database.connexion import Connexion

class StatistiqueDAO:

    def __init__(self):
        self.conn = Connexion().get_connexion()
        self.cursor = self.conn.cursor(dictionary=True)

    def incidents_par_statut(self):

        query = """
        SELECT statut,
               COUNT(*) total
        FROM incident
        GROUP BY statut
        """

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def incidents_par_priorite(self):

        query = """
        SELECT priorite,
               COUNT(*) total
        FROM incident
        GROUP BY priorite
        """

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def top_techniciens(self):

        query = """
        SELECT u.nom,
               u.prenom,
               COUNT(*) nb_interventions
        FROM intervention i
        JOIN utilisateur u
        ON u.id=i.technicien_id
        GROUP BY u.id
        ORDER BY nb_interventions DESC
        LIMIT 3
        """

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def temps_moyen_resolution(self):

        query = """
        SELECT AVG(duree_minutes)/60 moyenne_heures
        FROM intervention
        """

        self.cursor.execute(query)

        return self.cursor.fetchone()