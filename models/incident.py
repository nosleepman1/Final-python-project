
class Incident:

    def __init__(self, titre, description, priorite="MOYENNE", statut="OUVERT", utilisateur_id=None, id=None, date_creation=None):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.utilisateur_id = utilisateur_id
        self.date_creation = date_creation

    def __str__(self):
        date_str = str(self.date_creation)[:16] if self.date_creation else "N/A"
        return f"[Ticket #{self.id}] [{self.statut}] ({self.priorite}) {self.titre} - Créé le {date_str}"
