
from dao.utilisateur_dao import UtilisateurDAO
from dao.incident_dao import IncidentDAO
from dao.intervention_dao import InterventionDAO
from models.utilisateur import Utilisateur
from models.incident import Incident
from models.intervention import Intervention


def menu_utilisateur(utilisateur: Utilisateur):
    incident_dao = IncidentDAO()
    interv_dao = InterventionDAO()

    while True:
        print("\n" + "=" * 50)
        print(f"   ESPACE UTILISATEUR : {utilisateur.prenom} {utilisateur.nom}")
        print("=" * 50)
        print("1. Déclarer un nouvel incident")
        print("2. Consulter la liste de mes incidents")
        print("3. Voir le détail d'un incident (+ interventions)")
        print("4. Filtrer mes incidents par statut")
        print("5. Filtrer mes incidents par priorité")
        print("6. Annuler un incident (si OUVERT)")
        print("0. Déconnexion")
        print("-" * 50)

        choix = input("Votre choix : ").strip()

        if choix == "1":
            print("\n--- NOUVEL INCIDENT ---")
            titre = input("Titre de l'incident : ").strip()
            if not titre:
                print("Le titre ne peut pas être vide.")
                continue
            description = input("Description détaillée : ").strip()

            print("Priorités disponibles : 1. BASSE | 2. MOYENNE | 3. HAUTE | 4. CRITIQUE")
            p_choix = input("Choix priorité [défaut: 2] : ").strip()
            p_map = {"1": "BASSE", "2": "MOYENNE", "3": "HAUTE", "4": "CRITIQUE"}
            priorite = p_map.get(p_choix, "MOYENNE")

            nouvel_incident = Incident(
                titre=titre,
                description=description,
                priorite=priorite,
                statut="OUVERT",
                utilisateur_id=utilisateur.id
            )
            cree = incident_dao.add(nouvel_incident)
            if cree:
                print(f"[Succès] Ticket #{cree.id} créé avec succès !")
            else:
                print("[Erreur] Impossible d'enregistrer l'incident.")

        elif choix == "2":
            print("\n--- MES INCIDENTS ---")
            incidents = incident_dao.get_by_utilisateur(utilisateur.id)
            if not incidents:
                print("Vous n'avez déclaré aucun incident.")
            else:
                for inc in incidents:
                    print(inc)

        elif choix == "3":
            print("\n--- DÉTAIL D'UN INCIDENT ---")
            try:
                inc_id = int(input("ID du ticket : "))
                inc = incident_dao.get_by_id(inc_id)

                # Règle de sécurité : Seul le créateur ou technicien/admin peut voir le détail
                if not inc or inc.utilisateur_id != utilisateur.id:
                    print("[Erreur] Ticket introuvable ou vous n'avez pas l'autorisation d'y accéder.")
                else:
                    print("\n" + "-" * 40)
                    print(f"Ticket #{inc.id} : {inc.titre}")
                    print(f"Statut       : {inc.statut}")
                    print(f"Priorité     : {inc.priorite}")
                    print(f"Créé le      : {inc.date_creation}")
                    print(f"Description  : {inc.description}")
                    print("-" * 40)
                    print("Historique des interventions :")
                    interventions = interv_dao.get_by_incident(inc.id)
                    if not interventions:
                        print("  (Aucune intervention enregistrée pour le moment)")
                    else:
                        for itv in interventions:
                            print(f"  - {itv}")
            except ValueError:
                print("[Erreur] Veuillez entrer un identifiant numérique valide.")

        elif choix == "4":
            print("\n--- FILTRER PAR STATUT ---")
            print("1. OUVERT | 2. EN_COURS | 3. RESOLU | 4. FERME")
            s_choix = input("Choisissez le statut : ").strip()
            s_map = {"1": "OUVERT", "2": "EN_COURS", "3": "RESOLU", "4": "FERME"}
            statut = s_map.get(s_choix)
            if statut:
                incidents = incident_dao.get_by_utilisateur(utilisateur.id, statut=statut)
                if not incidents:
                    print(f"Aucun incident trouvé avec le statut '{statut}'.")
                else:
                    for inc in incidents:
                        print(inc)
            else:
                print("Choix de statut invalide.")

        elif choix == "5":
            print("\n--- FILTRER PAR PRIORITÉ ---")
            print("1. BASSE | 2. MOYENNE | 3. HAUTE | 4. CRITIQUE")
            p_choix = input("Choisissez la priorité : ").strip()
            p_map = {"1": "BASSE", "2": "MOYENNE", "3": "HAUTE", "4": "CRITIQUE"}
            priorite = p_map.get(p_choix)
            if priorite:
                incidents = incident_dao.get_by_utilisateur(utilisateur.id, priorite=priorite)
                if not incidents:
                    print(f"Aucun incident trouvé avec la priorité '{priorite}'.")
                else:
                    for inc in incidents:
                        print(inc)
            else:
                print("Choix de priorité invalide.")

        elif choix == "6":
            print("\n--- ANNULER UN INCIDENT ---")
            try:
                inc_id = int(input("ID du ticket à annuler : "))
                if incident_dao.annuler_incident(inc_id, utilisateur.id):
                    print(f"[Succès] Le ticket #{inc_id} a été annulé.")
                else:
                    print("[Erreur] Impossible d'annuler. L'incident n'existe pas ou n'est plus à l'état OUVERT.")
            except ValueError:
                print("[Erreur] Veuillez entrer un identifiant numérique valide.")

        elif choix == "0":
            print("\nDéconnexion en cours...")
            break
        else:
            print("Option non reconnue, veuillez réessayer.")


# 2. MENU TECHNICIEN

def menu_technicien(technicien: Utilisateur):
    incident_dao = IncidentDAO()
    interv_dao = InterventionDAO()

    while True:
        print("\n" + "=" * 50)
        print(f"   ESPACE TECHNICIEN : {technicien.prenom} {technicien.nom}")
        print("=" * 50)
        print("1. Consulter les incidents à traiter (OUVERT / EN_COURS)")
        print("2. Prendre en charge un incident (OUVERT -> EN_COURS)")
        print("3. Ajouter une intervention technique")
        print("4. Marquer un incident comme RESOLU")
        print("5. Fermer un incident résolu (RESOLU -> FERME)")
        print("6. Consulter mon historique d'interventions")
        print("0. Déconnexion")
        print("-" * 50)

        choix = input("Votre choix : ").strip()

        if choix == "1":
            print("\n--- INCIDENTS À TRAITER ---")
            incidents = incident_dao.get_incidents_actifs()
            if not incidents:
                print("Aucun incident ouvert ou en cours actuellement.")
            else:
                for inc in incidents:
                    print(inc)

        elif choix == "2":
            print("\n--- PRENDRE EN CHARGE UN INCIDENT ---")
            try:
                inc_id = int(input("ID de l'incident à prendre en charge : "))
                if incident_dao.prendre_en_charge(inc_id):
                    print(f"[Succès] Incident #{inc_id} pris en charge (Statut: EN_COURS).")
                else:
                    print("[Erreur] Impossible de prendre en charge. L'incident n'existe pas ou n'est pas au statut OUVERT.")
            except ValueError:
                print("[Erreur] ID invalide.")

        elif choix == "3":
            print("\n--- AJOUTER UNE INTERVENTION ---")
            try:
                inc_id = int(input("ID de l'incident : "))
                commentaire = input("Compte-rendu de l'intervention : ").strip()
                if not commentaire:
                    print("Le commentaire ne peut pas être vide.")
                    continue
                duree = int(input("Durée de l'intervention (en minutes) : "))
                if duree < 0:
                    print("La durée doit être un entier positif.")
                    continue

                nouvelle_interv = Intervention(
                    commentaire=commentaire,
                    duree_minutes=duree,
                    incident_id=inc_id,
                    technicien_id=technicien.id
                )
                creee = interv_dao.add(nouvelle_interv)
                if creee:
                    print(f"[Succès] Intervention enregistrée pour le ticket #{inc_id}.")
                else:
                    print("[Erreur] Impossible d'ajouter l'intervention.")
            except ValueError:
                print("[Erreur] Veuillez entrer des nombres entiers pour l'ID et la durée.")

        elif choix == "4":
            print("\n--- RÉSOUDRE UN INCIDENT ---")
            try:
                inc_id = int(input("ID de l'incident à marquer comme RESOLU : "))
                if incident_dao.resoudre_incident(inc_id):
                    print(f"[Succès] Incident #{inc_id} marqué comme RESOLU.")
                else:
                    print("[Erreur] L'incident doit être au statut 'EN_COURS' pour être résolu.")
            except ValueError:
                print("[Erreur] ID invalide.")

        elif choix == "5":
            print("\n--- FERMER UN INCIDENT ---")
            try:
                inc_id = int(input("ID de l'incident résolu à FERMER : "))
                if incident_dao.fermer_incident(inc_id):
                    print(f"[Succès] Incident #{inc_id} fermé définitivement.")
                else:
                    print("[Erreur] L'incident doit être au statut 'RESOLU' pour être fermé.")
            except ValueError:
                print("[Erreur] ID invalide.")

        elif choix == "6":
            print("\n--- MON HISTORIQUE D'INTERVENTIONS ---")
            interventions = interv_dao.get_by_technicien(technicien.id)
            if not interventions:
                print("Aucune intervention enregistrée à votre nom.")
            else:
                for itv in interventions:
                    print(itv)

        elif choix == "0":
            print("\nDéconnexion en cours...")
            break
        else:
            print("Option invalide.")



# 3. MENU ADMINISTRATEUR (Superviseur)

def menu_admin(admin: Utilisateur):
    user_dao = UtilisateurDAO()
    incident_dao = IncidentDAO()

    while True:
        print("\n" + "=" * 50)
        print(f"   ESPACE ADMINISTRATEUR : {admin.prenom} {admin.nom}")
        print("=" * 50)
        print("1. Gestion des Utilisateurs (CRUD & Recherche)")
        print("2. Consulter tous les incidents (Supervision)")
        print("3. Espace Technicien (Prendre en charge / Résoudre)")
        print("4. Statistiques et Rapports d'activité")
        print("0. Déconnexion")
        print("-" * 50)

        choix = input("Votre choix : ").strip()

        if choix == "1":
            _sous_menu_gestion_utilisateurs(user_dao)
        elif choix == "2":
            print("\n--- TOUS LES INCIDENTS (SUPERVISION) ---")
            incidents = incident_dao.get_all()
            if not incidents:
                print("Aucun incident en base de données.")
            else:
                for inc in incidents:
                    print(inc)
        elif choix == "3":
            # L'administrateur a accès aux fonctionnalités technicien
            menu_technicien(admin)
        elif choix == "4":
            _afficher_statistiques_admin(incident_dao)
        elif choix == "0":
            print("\nDéconnexion en cours...")
            break
        else:
            print("Option invalide.")


def _sous_menu_gestion_utilisateurs(dao: UtilisateurDAO):
    """Sous-menu dédié au CRUD complet des utilisateurs pour l'Admin."""
    while True:
        print("\n" + "-" * 45)
        print("   GESTION DES UTILISATEURS")
        print("-" * 45)
        print("1. Ajouter un utilisateur")
        print("2. Lister tous les utilisateurs")
        print("3. Rechercher un utilisateur (nom, login, service)")
        print("4. Modifier un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Retour au menu précédent")

        choix = input("Choix : ").strip()

        if choix == "1":
            print("\n--- NOUVEL UTILISATEUR ---")
            login = input("Login unique : ").strip()
            password = input("Mot de passe : ").strip()
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            email = input("Email : ").strip()
            print("Rôles : 1. UTILISATEUR | 2. TECHNICIEN | 3. ADMIN")
            r_choix = input("Choix rôle [défaut: 1] : ").strip()
            r_map = {"1": "UTILISATEUR", "2": "TECHNICIEN", "3": "ADMIN"}
            role = r_map.get(r_choix, "UTILISATEUR")
            service = input("Service : ").strip()

            u = Utilisateur(login, password, nom, prenom, email, role, service)
            if dao.add(u):
                print(f"[Succès] Utilisateur #{u.id} créé avec succès !")
            else:
                print("[Erreur] Impossible de créer cet utilisateur (login déjà existant ?).")

        elif choix == "2":
            print("\n--- LISTE DES UTILISATEURS ---")
            users = dao.get_all()
            for u in users:
                print(f"ID: {u.id:2d} | [{u.role:10s}] {u.prenom} {u.nom} (@{u.login}) - {u.service} ({u.email})")

        elif choix == "3":
            print("\n--- RECHERCHER UN UTILISATEUR ---")
            terme = input("Entrez un nom, login ou service : ").strip()
            resultats = dao.rechercher(terme)
            if not resultats:
                print(f"Aucun utilisateur trouvé pour '{terme}'.")
            else:
                for u in resultats:
                    print(f"ID: {u.id:2d} | [{u.role:10s}] {u.prenom} {u.nom} (@{u.login}) - {u.service}")

        elif choix == "4":
            print("\n--- MODIFIER UN UTILISATEUR ---")
            try:
                u_id = int(input("ID de l'utilisateur à modifier : "))
                u = dao.get_by_id(u_id)
                if not u:
                    print("Utilisateur introuvable.")
                else:
                    u.nom = input(f"Nouveau nom [{u.nom}] : ").strip() or u.nom
                    u.prenom = input(f"Nouveau prénom [{u.prenom}] : ").strip() or u.prenom
                    u.email = input(f"Nouveau email [{u.email}] : ").strip() or u.email
                    u.service = input(f"Nouveau service [{u.service}] : ").strip() or u.service
                    if dao.update(u):
                        print("[Succès] Utilisateur mis à jour.")
                    else:
                        print("[Erreur] Échec de la mise à jour.")
            except ValueError:
                print("[Erreur] ID invalide.")

        elif choix == "5":
            print("\n--- SUPPRIMER UN UTILISATEUR ---")
            try:
                u_id = int(input("ID de l'utilisateur à supprimer : "))
                u = dao.get_by_id(u_id)
                if not u:
                    print("Utilisateur introuvable.")
                else:
                    conf = input(f"Confirmer la suppression de {u.prenom} {u.nom} ? (o/n) : ").strip().lower()
                    if conf == 'o':
                        if dao.delete_by_id(u_id):
                            print("[Succès] Utilisateur supprimé.")
                        else:
                            print("[Avertissement] Suppression refusée (utilisateur lié à des incidents ou interventions).")
            except ValueError:
                print("[Erreur] ID invalide.")

        elif choix == "0":
            break


def _afficher_statistiques_admin(dao: IncidentDAO):
    """Affiche les 6 statistiques et rapports exigés par le sujet."""
    print("\n" + "=" * 55)
    print("        RAPPORTS ET STATISTIQUES D'ACTIVITÉ")
    print("=" * 55)

    # 1. Total par statut
    print("\n1. Nombre total d'incidents par statut :")
    stats_statut = dao.stats_par_statut()
    for statut, total in stats_statut:
        print(f"   - {statut:10s} : {total} ticket(s)")

    # 2. Total par priorité
    print("\n2. Nombre d'incidents par priorité :")
    stats_prio = dao.stats_par_priorite()
    for prio, total in stats_prio:
        print(f"   - {prio:10s} : {total} ticket(s)")

    # 3. Temps moyen de résolution
    temps_moyen = dao.temps_moyen_resolution_heures()
    print(f"\n3. Temps moyen de résolution par incident : {temps_moyen} heure(s)")

    # 4. Top 3 des techniciens les plus actifs
    print("\n4. Top 3 des techniciens les plus actifs :")
    top_techs = dao.top_3_techniciens()
    if not top_techs:
        print("   (Aucune intervention enregistrée)")
    else:
        for idx, (prenom, nom, nb) in enumerate(top_techs, 1):
            print(f"   {idx}. {prenom} {nom} - {nb} intervention(s)")

    # 5. Détail par technicien
    print("\n5. Statistiques détaillées par technicien :")
    tech_details = dao.stats_par_technicien()
    for prenom, nom, nb_inc, duree_moy in tech_details:
        print(f"   - {prenom} {nom} : {nb_inc} incident(s) traité(s) | Durée moyenne : {duree_moy} min/interv.")

    # 6. Taux de résolution en moins de 48h
    taux_48h = dao.taux_resolution_48h()
    print(f"\n6. Taux de résolution dans les 48h : {taux_48h}% des incidents résolus")
    print("=" * 55)