# dao/utilisateur_dao.py
from dao.base_dao import BaseDAO
from models.utilisateur import Utilisateur


class UtilisateurDAO(BaseDAO):

    def get_all(self):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return []
        utilisateurs = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur ORDER BY id ASC")
            for row in cursor.fetchall():
                utilisateurs.append(Utilisateur(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return utilisateurs

    def get_by_id(self, user_id):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return Utilisateur(**row)
        except Exception as e:
            print(f"Erreur lors de la récupération par ID : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def get_by_login(self, login):
        if not self.conn:
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE login = %s", (login,))
            row = cursor.fetchone()
            if row:
                return Utilisateur(**row)
        except Exception as e:
            print(f"Erreur lors de la recherche par login : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def delete_by_id(self, user_id):

        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()

            # Contrainte métier : vérifier s'il a créé des incidents
            cursor.execute("SELECT COUNT(*) FROM incident WHERE utilisateur_id = %s", (user_id,))
            (nb_incidents,) = cursor.fetchone()
            if nb_incidents > 0:
                print(f"[Avertissement] Impossible de supprimer : {nb_incidents} incident(s) sont liés à cet utilisateur.")
                return False

            # Contrainte métier : vérifier s'il a réalisé des interventions
            cursor.execute("SELECT COUNT(*) FROM intervention WHERE technicien_id = %s", (user_id,))
            (nb_interventions,) = cursor.fetchone()
            if nb_interventions > 0:
                print(f"[Avertissement] Impossible de supprimer : {nb_interventions} intervention(s) sont liées à cet utilisateur.")
                return False

            # Suppression effective
            cursor.execute("DELETE FROM utilisateur WHERE id = %s", (user_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def add(self, user: Utilisateur):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return None
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """INSERT INTO utilisateur 
                       (login, password, nom, prenom, email, role, service) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (user.login, user.password, user.nom, user.prenom, user.email, user.role, user.service)
            cursor.execute(query, values)
            self.conn.commit()
            user.id = cursor.lastrowid
            return user
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def update(self, user: Utilisateur):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """UPDATE utilisateur 
                       SET login=%s, password=%s, nom=%s, prenom=%s, email=%s, role=%s, service=%s 
                       WHERE id=%s"""
            values = (user.login, user.password, user.nom, user.prenom, user.email, user.role, user.service, user.id)
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la modification de l'utilisateur : {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()

    def authentifier(self, login, password):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = "SELECT * FROM utilisateur WHERE login = %s AND password = %s"
            cursor.execute(query, (login, password))
            row = cursor.fetchone()
            if row:
                return Utilisateur(**row)
        except Exception as e:
            print(f"Erreur lors de l'authentification : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def rechercher(self, mot_cle):
        if not self.conn:
            return []
        utilisateurs = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            pattern = f"%{mot_cle}%"
            query = """
            SELECT * FROM utilisateur 
            WHERE login LIKE %s OR nom LIKE %s OR prenom LIKE %s OR service LIKE %s
            ORDER BY id ASC
            """
            cursor.execute(query, (pattern, pattern, pattern, pattern))
            for row in cursor.fetchall():
                utilisateurs.append(Utilisateur(**row))
        except Exception as e:
            print(f"Erreur lors de la recherche d'utilisateurs : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return utilisateurs