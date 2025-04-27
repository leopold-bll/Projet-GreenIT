# GreunRunner

Projet de sensibilisation au Green-IT et IT for Green sous forme de quiz compétitif.
Développé dans le cadre du projet Green-IT par Harone Chitam, Léopold Billecocq, Ashraf Ait Abbas et Max Bortolotti.

## Description

GreunRunner est un site web léger conçu pour minimiser son empreinte environnementale.
Il propose deux quiz au choix (Green-IT ou IT for Green), avec un système de classement basé sur les scores obtenus.

## Fonctionnalités

- Création et connexion à un compte utilisateur
- Sélection entre deux types de quiz
- 10 questions par quiz
- Attribution d'un score et classement des joueurs
- Interface sobre et éco-conçue (sans images ni vidéos)
- Dashboard CRUD pour les utilisateurs admin

## Technologies utilisées

Frontend : HTML, CSS, JavaScript (sans framework)
Backend : Python (Flask)
Base de données : MySQL

---

## Instructions pour cloner, configurer et exécuter le projet

1. Cloner le projet :

git clone https://github.com/leopold-bll/Projet-GreenIT
cd Projet-GreenIT


2. Installer les dépendances :

pip install -r requirements.txt


3. Configurer la base de données MySQL :

Créer la base de données MySQL à partir des fichiers Create.sql et Insert.sql fournis.
Veilliez à ce que les identifiants, mots de passe, nom de connexion, et nom de schéma soient les mêmes dans MySQL Workbench et dans la ligne 9 du app.py.


5. Lancer le serveur Flask :

Exécuter le fichier app.py


6. Accéder au site :

Ouvrir votre navigateur et aller sur http://127.0.0.1:5000

---

## Contribuer au projet

Nous encourageons toute contribution respectant les règles suivantes :

1. Convention de nommage des commits :

feat: pour une nouvelle fonctionnalité
fix: pour une correction de bug
docs: pour la documentation
style: pour des changements de style (indentations, etc.)
refactor: pour des changements de structure de code sans changement de fonctionnalités
perf: pour des améliorations de performance
test: pour des ajouts de tests
chore: pour des tâches de maintenance


2. Workflow de contribution :

Forker le projet
Créer une branche dédiée :
git checkout -b feat/ma-nouvelle-fonctionnalite
Faire vos modifications
Faire une pull request
