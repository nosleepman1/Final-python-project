from datetime import datetime

class InterventionDAO(BaseDAO):

    def ajouter_intervention(
        self,
        commentaire,
        duree_minutes,
        incident_id,
        technicien_id
    ):

        query = """
        INSERT INTO intervention
        (
            commentaire,
            duree_minutes,
            date_intervention,
            incident_id,
            technicien_id
        )
        VALUES(%s,%s,%s,%s,%s)
        """

        self.cursor.execute(
            query,
            (
                commentaire,
                duree_minutes,
                datetime.now(),
                incident_id,
                technicien_id
            )
        )

        self.conn.commit()

    def historique_technicien(self, technicien_id):

        query = """
        SELECT *
        FROM intervention
        WHERE technicien_id=%s
        """

        self.cursor.execute(query, (technicien_id,))
        return self.cursor.fetchall()