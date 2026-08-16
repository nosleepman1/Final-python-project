# dao/incident_dao.py
from dao.base_dao import BaseDAO
from models.incident import Incident


class IncidentDAO(BaseDAO):


    def get_all(self):
        """Récupère l'ensemble des incidents."""
        if not self.conn:
            return []
        incidents = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM incident ORDER BY date_creation DESC")
            for row in cursor.fetchall():
                incidents.append(Incident(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des incidents : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return incidents

    def get_by_id(self, incident_id):
        if not self.conn:
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM incident WHERE id = %s", (incident_id,))
            row = cursor.fetchone()
            if row:
                return Incident(**row)
        except Exception as e:
            print(f"Erreur lors de la récupération de l'incident : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def delete_by_id(self, incident_id):

        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            # Vérification de la contrainte : pas d'intervention rattachée
            cursor.execute("SELECT COUNT(*) FROM intervention WHERE incident_id = %s", (incident_id,))
            (nb_interv,) = cursor.fetchone()
            if nb_interv > 0:
                print(f"[Avertissement] Impossible de supprimer : {nb_interv} intervention(s) liée(s) à cet incident.")
                return False

            cursor.execute("DELETE FROM incident WHERE id = %s", (incident_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la suppression de l'incident : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def add(self, incident: Incident):
        if not self.conn:
            return None
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
            INSERT INTO incident (titre, description, priorite, statut, utilisateur_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (incident.titre, incident.description, incident.priorite, incident.statut, incident.utilisateur_id)
            cursor.execute(query, values)
            self.conn.commit()
            incident.id = cursor.lastrowid
            return incident
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la création de l'incident : {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def get_by_utilisateur(self, utilisateur_id, statut=None, priorite=None):

        if not self.conn:
            return []
        incidents = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM incident WHERE utilisateur_id = %s"
            params = [utilisateur_id]

            if statut:
                query += " AND statut = %s"
                params.append(statut)
            if priorite:
                query += " AND priorite = %s"
                params.append(priorite)

            query += " ORDER BY date_creation DESC"
            cursor.execute(query, tuple(params))
            for row in cursor.fetchall():
                incidents.append(Incident(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des incidents utilisateur : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return incidents

    def get_incidents_actifs(self):
        if not self.conn:
            return []
        incidents = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM incident WHERE statut IN ('OUVERT', 'EN_COURS') ORDER BY date_creation ASC"
            cursor.execute(query)
            for row in cursor.fetchall():
                incidents.append(Incident(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des incidents actifs : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return incidents


    def prendre_en_charge(self, incident_id):
        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = "UPDATE incident SET statut = 'EN_COURS' WHERE id = %s AND statut = 'OUVERT'"
            cursor.execute(query, (incident_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la prise en charge : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def resoudre_incident(self, incident_id):

        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = "UPDATE incident SET statut = 'RESOLU' WHERE id = %s AND statut = 'EN_COURS'"
            cursor.execute(query, (incident_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la résolution de l'incident : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def fermer_incident(self, incident_id):

        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = "UPDATE incident SET statut = 'FERME' WHERE id = %s AND statut = 'RESOLU'"
            cursor.execute(query, (incident_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la fermeture de l'incident : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def annuler_incident(self, incident_id, utilisateur_id):

        if not self.conn:
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = "UPDATE incident SET statut = 'ANNULE' WHERE id = %s AND utilisateur_id = %s AND statut = 'OUVERT'"
            cursor.execute(query, (incident_id, utilisateur_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de l'annulation de l'incident : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()


    def stats_par_statut(self):
        if not self.conn:
            return []
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT statut, COUNT(*) FROM incident GROUP BY statut")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur stats statut : {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def stats_par_priorite(self):

        if not self.conn:
            return []
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT priorite, COUNT(*) FROM incident GROUP BY priorite")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur stats priorité : {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def top_3_techniciens(self):

        if not self.conn:
            return []
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
            SELECT u.prenom, u.nom, COUNT(i.id) AS nb_interventions
            FROM intervention i
            JOIN utilisateur u ON i.technicien_id = u.id
            GROUP BY u.id, u.prenom, u.nom
            ORDER BY nb_interventions DESC
            LIMIT 3
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur stats top techniciens : {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def stats_par_technicien(self):

        if not self.conn:
            return []
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
            SELECT u.prenom, u.nom, 
                   COUNT(DISTINCT i.incident_id) AS nb_incidents,
                   IFNULL(ROUND(AVG(i.duree_minutes), 1), 0) AS duree_moyenne_min
            FROM utilisateur u
            LEFT JOIN intervention i ON u.id = i.technicien_id
            WHERE u.role = 'TECHNICIEN'
            GROUP BY u.id, u.prenom, u.nom
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur stats par technicien : {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def temps_moyen_resolution_heures(self):

        if not self.conn:
            return 0.0
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
            SELECT IFNULL(AVG(TIMESTAMPDIFF(HOUR, inc.date_creation, MAX_INT.max_date)), 0)
            FROM incident inc
            JOIN (
                SELECT incident_id, MAX(date_intervention) AS max_date
                FROM intervention
                GROUP BY incident_id
            ) AS MAX_INT ON inc.id = MAX_INT.incident_id
            WHERE inc.statut IN ('RESOLU', 'FERME')
            """
            cursor.execute(query)
            (result,) = cursor.fetchone()
            return round(float(result), 2)
        except Exception as e:
            print(f"Erreur calcul temps moyen : {e}")
            return 0.0
        finally:
            if cursor is not None:
                cursor.close()

    def taux_resolution_48h(self):

        if not self.conn:
            return 0.0
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
            SELECT 
                COUNT(CASE WHEN TIMESTAMPDIFF(HOUR, inc.date_creation, MAX_INT.max_date) <= 48 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0)
            FROM incident inc
            JOIN (
                SELECT incident_id, MAX(date_intervention) AS max_date
                FROM intervention
                GROUP BY incident_id
            ) AS MAX_INT ON inc.id = MAX_INT.incident_id
            WHERE inc.statut IN ('RESOLU', 'FERME')
            """
            cursor.execute(query)
            (result,) = cursor.fetchone()
            return round(float(result), 2) if result is not None else 0.0
        except Exception as e:
            print(f"Erreur taux 48h : {e}")
            return 0.0
        finally:
            if cursor is not None:
                cursor.close()