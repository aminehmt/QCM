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
