class Intervention:
    
    def __init__(self, commentaire, duree_minutes, incident_id, technicien_id, id=None, date_intervention=None):
        self.id = id
        self.commentaire = commentaire
        self.duree_minutes = int(duree_minutes) if duree_minutes is not None else 0
        self.incident_id = incident_id
        self.technicien_id = technicien_id
        self.date_intervention = date_intervention

    def __str__(self):
        date_str = str(self.date_intervention)[:16] if self.date_intervention else "N/A"
        return f"[Intervention #{self.id}] Incident #{self.incident_id} | Durée: {self.duree_minutes} min | Date: {date_str}\n  >> {self.commentaire}"
