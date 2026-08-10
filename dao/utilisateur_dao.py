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
            cursor.execute("SELECT * FROM utilisateur")
            for row in cursor.fetchall():
                utilisateurs.append(Utilisateur(**row))
        except Exception as e:
            print(f"Erreur lors de la récupération : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return utilisateurs

    def get_by_id(self, id):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return None
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                return Utilisateur(**row)
        except Exception as e:
            print(f"Erreur lors de la récupération : {e}")
        finally:
            if cursor is not None:
                cursor.close()
        return None

    def delete_by_id(self, id):
        if not self.conn:
            print("Erreur : Connexion à la base de données indisponible.")
            return False
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM utilisateur WHERE id = %s", (id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Erreur lors de la suppression : {e}")
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
            print(f"Erreur lors de l'ajout : {e}")
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
            print(f"Erreur lors de la modification : {e}")
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