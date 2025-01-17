import json
import os
import csv
from datetime import datetime
import signal

def charger_utilisateurs(): #fonction pour utilisateurs
    if os.path.exists('users.json'): #il faut cree le fichier users.json par la suite
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}

def sauvegarder_utilisateurs(users): #fonction pour sauvegarder les utilisateurs
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def authentification(users):   #fonction pour la connexion
    identifiant = input("Entrez votre identifiant : ")
    if identifiant in users:
        print(f"Bienvenue de retour, {identifiant} ! Voici votre historique :")
        for i, test in enumerate(users[identifiant]["historique"], 1):
            print(f"{i}. {test['date']} - Score : {test['score']}")
    else:
        print("Nouvel utilisateur détecté. Création du profil...")
        users[identifiant] = {"historique": []}
    return identifiant
#normalement tout est clair hena
def charger_questions(categorie=None): #et had la fct pour charger les questiosn depuis un fichier questions.json
    try:
        with open('questions.json', 'r') as file:
            questions = json.load(file)["questions"]
            if categorie:
                questions = [q for q in questions if q.get("categorie") == categorie]
            return questions
    except FileNotFoundError:
        print("Erreur : Le fichier questions.json est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur : Le fichier questions.json est corrompu.")
        return []
    #si vous avez des qst 9oloLI 