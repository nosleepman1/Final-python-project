# menu/auth.py
import sys
from dao.utilisateur_dao import UtilisateurDAO


def se_connecter():
    """
    Gère l'authentification de l'utilisateur en console.
    Retourne l'objet Utilisateur si connexion réussie, ou quitte l'application si l'utilisateur choisit 0.
    """
    dao = UtilisateurDAO()

    if not dao.conn:
        print("\n" + "=" * 55)
        print("  [ERREUR CRITIQUE] CONNEXION À MYSQL IMPOSSIBLE")
        print("=" * 55)
        print("Veuillez vous assurer que :")
        print(" 1. Votre serveur MySQL (Laragon / XAMPP) est bien démarré.")
        print(" 2. Les identifiants dans 'database/config.py' sont corrects.")
        print(" 3. Vous avez bien exécuté 'python create_tables.py'.")
        print("=" * 55)
        sys.exit(1)

    while True:
        print("\n" + "=" * 50)
        print("    APPLICATION DE GESTION DES INCIDENTS (HELP DESK)")
        print("                 AUTHENTIFICATION")
        print("=" * 50)
        print("Entrez vos identifiants ou tapez '0' pour quitter.")

        try:
            login = input("Identifiant (login) : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            sys.exit(0)

        if login == "0":
            print("\nAu revoir !")
            sys.exit(0)

        try:
            password = input("Mot de passe        : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            sys.exit(0)

        utilisateur = dao.authentifier(login, password)
        if utilisateur:
            print(f"\n[Succès] Connexion réussie ! Bienvenue {utilisateur.prenom} {utilisateur.nom} (Rôle : {utilisateur.role})")
            return utilisateur
        else:
            print("\n[Erreur] Login ou mot de passe incorrect. Veuillez réessayer.")
