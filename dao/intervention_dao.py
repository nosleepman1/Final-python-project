from dao.base_dao import BaseDAO
from models.intervention import Intervention


class InterventionDAO(BaseDAO):

    def get_all(self):
        if not self.conn:
            return []
        interventions = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM intervention ORDER BY date_intervention DESC")
            for row in cursor.fetchall():
                interventions.append(Intervention(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des interventions : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return interventions

    def get_by_id(self, intervention_id):
        """Récupère une intervention par son ID."""
        if not self.conn:
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM intervention WHERE id = %s", (intervention_id,))
            row = cursor.fetchone()
            if row:
                return Intervention(**row)
        except Exception as e:
            print(f"Erreur lors de la récupération de l'intervention : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def delete_by_id(self, intervention_id):
        """Supprime une intervention par son ID."""
        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM intervention WHERE id = %s", (intervention_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la suppression de l'intervention : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def add(self, intervention: Intervention):
        if not self.conn:
            return None
        cursor = None
        try:
            cursor = self.conn.cursor()

            # Vérification du statut de l'incident
            cursor.execute("SELECT statut FROM incident WHERE id = %s", (intervention.incident_id,))
            res = cursor.fetchone()
            if not res:
                print("[Erreur] L'incident spécifié n'existe pas.")
                return None

            statut_actuel = res[0]
            if statut_actuel not in ('OUVERT', 'EN_COURS'):
                print(f"[Avertissement] Impossible d'ajouter une intervention : l'incident est déjà '{statut_actuel}'.")
                return None

            query = """
            INSERT INTO intervention (commentaire, duree_minutes, incident_id, technicien_id)
            VALUES (%s, %s, %s, %s)
            """
            values = (intervention.commentaire, intervention.duree_minutes, intervention.incident_id, intervention.technicien_id)
            cursor.execute(query, values)
            self.conn.commit()
            intervention.id = cursor.lastrowid
            return intervention
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de l'ajout de l'intervention : {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def get_by_incident(self, incident_id):
        if not self.conn:
            return []
        interventions = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM intervention WHERE incident_id = %s ORDER BY date_intervention ASC", (incident_id,))
            for row in cursor.fetchall():
                interventions.append(Intervention(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des interventions de l'incident : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return interventions

    def get_by_technicien(self, technicien_id):

        if not self.conn:
            return []
        interventions = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM intervention WHERE technicien_id = %s ORDER BY date_intervention DESC", (technicien_id,))
            for row in cursor.fetchall():
                interventions.append(Intervention(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des interventions du technicien : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return interventions