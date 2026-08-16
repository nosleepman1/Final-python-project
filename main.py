# main.py
from menu.utilisateur_menu import UtilisateurMenu


def main():
    app = UtilisateurMenu()
    app.afficher_menu_principal()


if __name__ == "__main__":
    main()


