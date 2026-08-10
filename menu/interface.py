def menu_technicien():
    while True:
        print("\n=== MENU TECHNICIEN ===")
        print("1. Voir incidents")
        print("2. Prendre en charge incident")
        print("0. Retour")

        choix = input("Choix : ")

        if choix == "1":
            afficher_incidents()

        elif choix == "2":
            incident_id = int(input("ID Incident : "))
            dao = IncidentDAO()
            dao.prendre_en_charge(incident_id)
            print("Incident pris en charge")

        elif choix == "3":

            incident_id = int(input("ID Incident : "))
            commentaire = input("Commentaire : ")
            duree = int(input("Durée : "))

            intervention_dao.ajouter_intervention(
                commentaire,
                duree,
                incident_id,
                utilisateur_connecte.id
            )

        elif choix == "4":

            incident_id = int(input("ID Incident : "))
            incident_dao.resoudre_incident(incident_id)

            print("Incident résolu")