# models/utilisateur.py

class Utilisateur:
    def __init__(self, login, password, nom, prenom, email, role, service, id=None, date_creation=None):
        self.id = id
        self.login = login
        self.password = password
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.role = role
        self.service = service
        self.date_creation = date_creation

    def __str__(self):
        return f"[{self.role}] {self.prenom} {self.nom} (@{self.login}) - Service: {self.service}"