# menu/utilisateur_menu.py
from dao.utilisateur_dao import UtilisateurDAO
from models.utilisateur import Utilisateur


def afficher_menu_utilisateur():
    dao = UtilisateurDAO()

    while True:
        print("\n" + "=" * 40)
        print("     GESTION DES UTILISATEURS (CRUD)    ")
        print("=" * 40)
        print("1. Lister tous les utilisateurs")
        print("2. Chercher un utilisateur par ID")
        print("3. Ajouter un nouvel utilisateur")
        print("4. Modifier un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Retour au menu principal")

        choix = input("\nChoix : ").strip()

        if choix == "1":
            print("\n--- Liste des utilisateurs ---")
            users = dao.get_all()
            if not users:
                print("Aucun utilisateur trouvé.")
            for u in users:
                print(u)

        elif choix == "2":
            try:
                user_id = int(input("Entrez l'ID de l'utilisateur : "))
                user = dao.get_by_id(user_id)
                if user:
                    print(f"\nTrouvé : {user}")
                else:
                    print("Utilisateur introuvable.")
            except ValueError:
                print("ID invalide.")

        elif choix == "3":
            print("\n--- Ajout d'un nouvel utilisateur ---")
            login = input("Login : ").strip()
            password = input("Mot de passe : ").strip()
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            email = input("Email : ").strip()

            print("Rôles disponibles : 1. UTILISATEUR | 2. TECHNICIEN | 3. ADMIN")
            role_choix = input("Choisissez le rôle (1-3) : ").strip()
            roles = {"1": "UTILISATEUR", "2": "TECHNICIEN", "3": "ADMIN"}
            role = roles.get(role_choix, "UTILISATEUR")

            service = input("Service (ex: Informatique, RH, Comptabilité) : ").strip()

            nouveau_user = Utilisateur(login, password, nom, prenom, email, role, service)
            res = dao.add(nouveau_user)
            if res:
                print(f"Utilisateur {res.login} créé avec succès (ID: {res.id}) !")
            else:
                print("Échec de la création.")

        elif choix == "4":
            try:
                user_id = int(input("ID de l'utilisateur à modifier : "))
                user = dao.get_by_id(user_id)
                if not user:
                    print("Utilisateur introuvable.")
                    continue

                print(f"Modification de {user.login} (Laissez vide pour conserver la valeur actuelle)")
                login = input(f"Nouveau login [{user.login}] : ").strip() or user.login
                password = input(f"Nouveau password : ").strip() or user.password
                nom = input(f"Nouveau nom [{user.nom}] : ").strip() or user.nom
                prenom = input(f"Nouveau prénom [{user.prenom}] : ").strip() or user.prenom
                email = input(f"Nouvel email [{user.email}] : ").strip() or user.email
                service = input(f"Nouveau service [{user.service}] : ").strip() or user.service

                user.login = login
                user.password = password
                user.nom = nom
                user.prenom = prenom
                user.email = email
                user.service = service

                if dao.update(user):
                    print("Utilisateur mis à jour avec succès !")
                else:
                    print("Échec de la mise à jour.")

            except ValueError:
                print("ID invalide.")

        elif choix == "5":
            try:
                user_id = int(input("ID de l'utilisateur à supprimer : "))
                # La suppression échouera automatiquement en BD s'il a des incidents/interventions liées
                if dao.delete_by_id(user_id):
                    print("Utilisateur supprimé avec succès.")
                else:
                    print(
                        "Impossible de supprimer cet utilisateur (il est probablement lié à un incident/intervention).")
            except ValueError:
                print("ID invalide.")

        elif choix == "0":
            break
        else:
            print("Choix invalide, réessayez.")