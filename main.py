# main.py
from menu.auth import se_connecter
from menu.interface import menu_utilisateur, menu_technicien, menu_admin


def main():
    while True:
        # Étape 1 : Authentification obligatoire
        utilisateur = se_connecter()

        # Étape 2 : Aiguillage vers le menu adapté selon le rôle
        if utilisateur.role == "ADMIN":
            menu_admin(utilisateur)
        elif utilisateur.role == "TECHNICIEN":
            menu_technicien(utilisateur)
        elif utilisateur.role == "UTILISATEUR":
            menu_utilisateur(utilisateur)
        else:
            print(f"[Erreur] Rôle inconnu : {utilisateur.role}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur. Fermeture de l'application.")
