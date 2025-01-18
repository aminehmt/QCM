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

def limite_temps(signum, frame): #timeout ida marepondach f le temps alloué 
    raise TimeoutError("Temps écoulé pour cette question.")

def passer_test(questions, limite_par_question=30): 
    signal.signal(signal.SIGALRM, limite_temps)
    score = 0
    #print question
    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{j + 1}. {option}")
        try:
            #timer 
            signal.alarm(limite_par_question)
            reponse = int(input("Votre réponse (1-4) : ")) - 1
            signal.alarm(0) #reponda a temps desactiver timer
            if reponse == q['reponse']:
                print("Correct ! ")
                score += 1
            else:
                print(f"Incorrect . La bonne réponse était : {q['options'][q['reponse']]}")
        except TimeoutError: #depassa le temps 
            print("\nTemps écoulé pour cette question. Passons à la suivante.")
            signal.alarm(0)
    return score

def enregistrer_resultat(users, identifiant, score): #save resultat bch thato f fichier
    users[identifiant]["historique"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score
    })
    sauvegarder_utilisateurs(users)
