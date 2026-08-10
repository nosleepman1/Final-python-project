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