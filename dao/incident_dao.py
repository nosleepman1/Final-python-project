class IncidentDAO(BaseDAO):

    def get_incidents_ouverts_encours(self):
        query = """
        SELECT * FROM incident
        WHERE statut IN ('OUVERT', 'EN_COURS')
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def prendre_en_charge(self, incident_id):
        query = """
        UPDATE incident
        SET statut='EN_COURS'
        WHERE id=%s
        AND statut='OUVERT'
        """
        self.cursor.execute(query, (incident_id,))
        self.conn.commit()

    def fermer_incident(self, incident_id):
        query = """
        UPDATE incident
        SET statut='FERME'
        WHERE id=%s
        AND statut='RESOLU'
        """
        self.cursor.execute(query, (incident_id,))
        self.conn.commit()

def resoudre_incident(self, incident_id):

    query = """
    UPDATE incident
    SET statut='RESOLU'
    WHERE id=%s
    AND statut='EN_COURS'
    """

    self.cursor.execute(query, (incident_id,))
    self.conn.commit()