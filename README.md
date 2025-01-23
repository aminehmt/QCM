# Projet de QCM 

Ce projet est une application interactive de quiz qui permet aux utilisateurs de répondre à des questions, de suivre leur historique de scores et d'exporter les résultats. Il offre également la possibilité de choisir des catégories spécifiques de questions et de gérer un chronomètre par question.

## Fonctionnalités

- **Authentification utilisateur** : Les utilisateurs peuvent s'authentifier avec un identifiant unique. Les nouveaux utilisateurs sont automatiquement ajoutés.
- **Gestion des catégories** : Les utilisateurs peuvent choisir une catégorie spécifique ou répondre à des questions de toutes les catégories disponibles.
- **Chronomètre** : Chaque question est limitée dans le temps (par défaut : 30 secondes).
- **Suivi des scores** : L'historique des scores est sauvegardé pour chaque utilisateur.
- **Export des résultats** : Les scores sont exportables au format CSV.

## Prérequis

- Python 3.x
- Bibliothèques standards Python (json, os, csv, datetime, signal, threading)

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers nécessaires.
2. Assurez-vous que les fichiers suivants sont présents dans le dossier du projet :
   - `main.py` (le script principal)
   - `users.json` (pour sauvegarder les données utilisateur, sera créé automatiquement s'il n'existe pas)
   - `questions.json` (doit contenir les questions au format JSON)

## Exemple d'exécution

Entrez votre identifiant : 23
Nouvel utilisateur détecté. Création du profil...

Catégories disponibles 😊
1. Bases de données
2. Réseaux
3. Python
4. Algorithmes

Choisissez une catégorie (ou appuyez sur Entrée pour toutes) : 2

Vous avez 30 secondes par question. Bonne chance !

Question 1: Quel protocole est utilisé pour envoyer des emails ?
1. HTTP
2. SMTP
3. FTP
4. IMAP
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 1
Incorrect ❌. La bonne réponse était : SMTP

Question 2: Quelle est la taille maximale d'un paquet IP ?
1. 64 KB
2. 32 KB
3. 128 KB
4. 16 KB
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 2
Incorrect ❌. La bonne réponse était : 64 KB

Question 3: Quel est le port par défaut pour HTTPS ?
1. 21
2. 22
3. 80
4. 443
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 1
Incorrect ❌. La bonne réponse était : 443

Question 4: Quel est le rôle du protocole DNS ?
1. Attribuer des adresses IP
2. Convertir les noms de domaine en adresses IP
3. Établir une connexion sécurisée
4. Transférer des fichiers
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 3
Incorrect ❌. La bonne réponse était : Convertir les noms de domaine en adresses IP

Question 5: Quelle commande permet de vérifier la connectivité réseau ?
1. ping
2. ls
3. grep
4. netstat
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 4
Incorrect ❌. La bonne réponse était : ping

Question 6: Quel modèle est utilisé pour les protocoles réseau ?
1. TCP/IP
2. OSI
3. HTTP
4. UDP
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 2
Correct ! ✅

Question 7: Quel est le rôle d'un switch dans un réseau ?
1. Fournir une connexion internet
2. Répéter le signal
3. Transférer des données entre les appareils
4. Convertir les adresses IP
Vous avez 30 secondes pour répondre.
Votre réponse (1-4) : 1
Incorrect ❌. La bonne réponse était : Transférer des données entre les appareils

Temps total pour compléter le test : 6.36 secondes

Score final : 1/7

Historique mis à jour 😊
1. 2025-01-23 08:30:48 - Score : 1 - Temps : 6.36 secondes
Résultats exportés dans le fichier resultats.csv.

### Exemple de fichier `questions.json`
```json
{
    "questions": [
      {
        "question": "Quelle méthode est utilisée pour ajouter un élément à une liste en Python ?",
        "options": ["add()", "append()", "push()", "insert()"],
        "reponse": 1,
        "categorie": "Python"
    },
    {
        "question": "Comment afficher 'Bonjour' en Python ?",
        "options": ["echo 'Bonjour'", "print('Bonjour')", "printf('Bonjour')", "cout << 'Bonjour'"],
        "reponse": 1,
        "categorie": "Python"
    },

    ]
}