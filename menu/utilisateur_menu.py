# menu/utilisateur_menu.py
import sys
from dao.utilisateur_dao import UtilisateurDAO
from models.utilisateur import Utilisateur


class UtilisateurMenu:
    def __init__(self):
        self.dao = UtilisateurDAO()

    def afficher_entete(self):
        print("\n" + "=" * 45)
        print("      SYSTEME DE GESTION DES UTILISATEURS")
        print("=" * 45)
        print("1. Ajouter un nouvel utilisateur")
        print("2. Lister tous les utilisateurs")
        print("3. Rechercher un utilisateur par ID")
        print("4. Modifier un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Quitter l'application")
        print("-" * 45)

    def afficher_menu_principal(self):
        while True:
            self.afficher_entete()
            choix = input("Votre choix (0-5) : ").strip()

            if choix == "1":
                self._ajouter_utilisateur()
            elif choix == "2":
                self._lister_utilisateurs()
            elif choix == "3":
                self._rechercher_utilisateur()
            elif choix == "4":
                self._modifier_utilisateur()
            elif choix == "5":
                self._supprimer_utilisateur()
            elif choix == "0":
                print("\nFermeture de l'application. Au revoir !")
                sys.exit(0)
            else:
                print("Choix invalide. Veuillez saisir un nombre entre 0 et 5.")

    def _ajouter_utilisateur(self):
        print("\n--- AJOUT D'UN UTILISATEUR ---")
        login = input("Login : ").strip()
        password = input("Mot de passe : ").strip()
        nom = input("Nom : ").strip()
        prenom = input("Prénom : ").strip()
        email = input("Email : ").strip()

        print("\nRôles disponibles : 1. UTILISATEUR | 2. TECHNICIEN | 3. ADMIN")
        role_choix = input("Choisissez le rôle (1-3) [défaut: 1] : ").strip()
        roles_map = {"1": "UTILISATEUR", "2": "TECHNICIEN", "3": "ADMIN"}
        role = roles_map.get(role_choix, "UTILISATEUR")

        service = input("Service : ").strip()

        nouvel_user = Utilisateur(
            login=login,
            password=password,
            nom=nom,
            prenom=prenom,
            email=email,
            role=role,
            service=service
        )

        if self.dao.add(nouvel_user):
            print("Utilisateur créé avec succès !")
        else:
            print("Échec de la création (login déjà existant ou erreur BDD).")

    def _lister_utilisateurs(self):
        print("\n--- LISTE DES UTILISATEURS ---")
        utilisateurs = self.dao.get_all()
        if not utilisateurs:
            print("Aucun utilisateur trouvé.")
        else:
            for u in utilisateurs:
                print(f"ID: {u.id:2d} | [{u.role:10s}] {u.prenom} {u.nom} (@{u.login}) - Service: {u.service}")

    def _rechercher_utilisateur(self):
        print("\n--- RECHERCHER UN UTILISATEUR ---")
        try:
            user_id = int(input("Entrez l'ID de l'utilisateur : "))
            u = self.dao.get_by_id(user_id)
            if u:
                print(f"\nID : {u.id}\nLogin : {u.login}\nNom complet : {u.prenom} {u.nom}\nEmail : {u.email}\nRôle : {u.role}\nService : {u.service}")
            else:
                print(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
        except ValueError:
            print("Erreur : L'ID doit être un nombre entier.")

    def _modifier_utilisateur(self):
        print("\n--- MODIFIER UN UTILISATEUR ---")
        try:
            user_id = int(input("Entrez l'ID de l'utilisateur à modifier : "))
            u = self.dao.get_by_id(user_id)
            if u:
                nom = input(f"Nouveau nom [{u.nom}] : ").strip() or u.nom
                prenom = input(f"Nouveau prénom [{u.prenom}] : ").strip() or u.prenom
                email = input(f"Nouveau email [{u.email}] : ").strip() or u.email
                service = input(f"Nouveau service [{u.service}] : ").strip() or u.service

                u.nom = nom
                u.prenom = prenom
                u.email = email
                u.service = service

                if self.dao.update(u):
                    print("Utilisateur mis à jour avec succès !")
                else:
                    print("Échec de la mise à jour.")
            else:
                print(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
        except ValueError:
            print("Erreur : L'ID doit être un nombre entier.")

    def _supprimer_utilisateur(self):
        print("\n--- SUPPRIMER UN UTILISATEUR ---")
        try:
            user_id = int(input("Entrez l'ID de l'utilisateur à supprimer : "))
            u = self.dao.get_by_id(user_id)
            if u:
                conf = input(f"Confirmer la suppression de {u.prenom} {u.nom} ? (o/n) : ").strip().lower()
                if conf == 'o':
                    if self.dao.delete_by_id(user_id):
                        print("Utilisateur supprimé avec succès !")
                    else:
                        print("Impossible de supprimer cet utilisateur.")
            else:
                print(f"Aucun utilisateur trouvé avec l'ID {user_id}.")
        except ValueError:
            print("Erreur : L'ID doit être un nombre entier.")