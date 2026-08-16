# Application de Gestion des Tickets d'Incidents (Help Desk)

Projet académique de programmation **Python (POO)** et **Base de données relationnelle MySQL**.  
**Établissement :** GROUPE ISI — Licence 2 Génie Logiciel (GL)  
**Enseignant :** M. DIALLO (`Muuustafa`)

---

## Membres du Groupe
* **Membre 1 :** [Nom & Prénom] (Chef de projet)
* **Membre 2 :** [Nom & Prénom]
* **Membre 3 :** [Nom & Prénom] *(si trinôme)*

---

## Présentation du Projet

La Direction des Systèmes d’Information (DSI) souhaite centraliser et automatiser la gestion des incidents informatiques. Cette application console en Python permet :
* **Aux utilisateurs (demandeurs)** : de déclarer des incidents, suivre l'avancement de leurs tickets et filtrer par statut ou priorité.
* **Aux techniciens** : de prendre en charge les incidents ouverts, d'enregistrer des comptes-rendus d'interventions techniques avec la durée, et de résoudre/fermer les tickets.
* **À l'administrateur** : de superviser la totalité des tickets, de gérer les comptes utilisateurs (CRUD complet avec contrôle d'intégrité) et de consulter les rapports statistiques et indicateurs de performance (KPIs).

---

## Architecture du Projet

Le projet applique le patron de conception **DAO (Data Access Object)** et sépare strictement les responsabilités :

```
gestion_incidents/
│
├── schema.sql                 # Script SQL complet (Création DB, tables et Seeders)
├── create_tables.py           # Script de migration Python (création des tables)
├── insert_test_data.py        # Script d'amorçage Python (données de test)
├── main.py                    # Point d'entrée principal
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation du projet
│
├── database/
│   ├── config.py              # Paramètres de connexion MySQL (hôte, port, mot de passe)
│   └── connexion.py           # Gestionnaire de connexion Singleton (instance unique)
│
├── models/
│   ├── utilisateur.py         # Modèle Utilisateur
│   ├── incident.py            # Modèle Incident
│   └── intervention.py        # Modèle Intervention
│
├── dao/
│   ├── base_dao.py            # Classe abstraite BaseDAO avec méthodes génériques
│   ├── utilisateur_dao.py     # CRUD Utilisateur, authentification et recherche
│   ├── incident_dao.py        # CRUD Incident, workflow des statuts et statistiques
│   └── intervention_dao.py    # CRUD Intervention et historique technicien
│
└── menu/
    ├── auth.py                # Écran d'authentification console
    └── interface.py           # Menus interactifs adaptés à chaque rôle
```

---

## Workflow des Statuts d'un Incident

Les transitions de statuts respectent scrupuleusement le cycle de vie suivant :

$$\text{OUVERT} \xrightarrow{\text{Prise en charge}} \text{EN\_COURS} \xrightarrow{\text{Résolution}} \text{RESOLU} \xrightarrow{\text{Fermeture}} \text{FERME}$$

> **Règle d'intégrité :** Le statut d'un incident ne peut jamais régresser (ex : un incident `RESOLU` ne peut pas repasser à `EN_COURS`).

---

## Prérequis et Installation

### 1. Prérequis
* **Python 3.8+**
* Un serveur **MySQL** ou **MariaDB** (via Laragon, XAMPP, WampServer ou Docker).

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration de la base de données
Vérifiez ou adaptez les identifiants dans le fichier `database/config.py` :
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',         # Ex: 'root' ou mot de passe vide selon votre environnement
    'database': 'gestion_incidents',
    'port': 3306
}
```

---

## Initialisation et Démarrage

### Étape 1 : Créer les tables (Migration)
Exécutez le script de création automatique des tables :
```bash
python create_tables.py
```
*(Ou importez directement le fichier `schema.sql` dans votre gestionnaire MySQL / phpMyAdmin).*

### Étape 2 : Insérer le jeu de données de test (Seeder)
```bash
python insert_test_data.py
```

### Étape 3 : Lancer l'application
```bash
python main.py
```

---

## Comptes de Test Pré-configurés

| Identifiant (Login) | Mot de passe | Rôle | Description / Service |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | **ADMIN** | Direction (accès total, CRUD utilisateurs, statistiques) |
| `tech1` | `tech123` | **TECHNICIEN** | Support Informatique (prise en charge & interventions) |
| `tech2` | `tech123` | **TECHNICIEN** | Réseaux & Télécoms |
| `user1` | `user123` | **UTILISATEUR** | Service Comptabilité (déclaration de tickets) |
| `user2` | `user123` | **UTILISATEUR** | Service Ressources Humaines |

---

## Statistiques Administrateur Disponibles

L'administrateur a accès en temps réel aux indicateurs clés (KPIs) :
1. Répartition du volume total d'incidents par **statut** (`OUVERT`, `EN_COURS`, `RESOLU`, `FERME`).
2. Répartition des incidents par niveau de **priorité** (`BASSE`, `MOYENNE`, `HAUTE`, `CRITIQUE`).
3. **Temps moyen de résolution** par incident (en heures).
4. **Top 3** des techniciens les plus actifs (par volume d'interventions).
5. Tableau de performance par technicien (nombre d'incidents résolus et durée moyenne par intervention).
6. **Taux de résolution dans les 48 heures** (% des incidents résolus en moins de deux jours).
