import json
import os
import csv
from datetime import datetime
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(script_dir, 'users.json')
questions_file = os.path.join(script_dir, 'questions.json')

def charger_utilisateurs():
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Erreur : Le fichier users.json est corrompu. Voulez-vous le réinitialiser ? (O/N)")
                choix = input().strip().lower()
                if choix == 'o':
                    return {}
                else:
                    print("Fermeture de l'application.")
                    exit()
    return {}

def authentification(users):
    while True:
        identifiant = input("Entrez votre identifiant : ").strip()
        if identifiant:
            if identifiant in users:
                print(f"Bienvenue de retour, {identifiant} ! Voici votre historique :")
                for i, test in enumerate(users[identifiant]["historique"], 1):
                    print(f"{i}. {test['date']} - Score : {test['score']}")
            else:
                print("Nouvel utilisateur détecté. Création du profil...")
                users[identifiant] = {"historique": []}
            return identifiant
        else:
            print("L'identifiant ne peut pas être vide. Réessayez.")

def limite_temps_timer(timer_expired_event):
    timer_expired_event.set()



def enregistrer_resultat(users, identifiant, score):
    users[identifiant]["historique"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score
    })
    sauvegarder_utilisateurs(users)

def main():
    users = charger_utilisateurs()
    identifiant = authentification(users)
    print("\nCatégories disponibles 😊")
    categories = set([q["categorie"] for q in charger_questions() if "categorie" in q])
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    choix_categorie = input("\nChoisissez une catégorie (ou appuyez sur Entrée pour toutes) : ")
    categorie = None
    if choix_categorie.isdigit() and 1 <= int(choix_categorie) <= len(categories):
        categorie = list(categories)[int(choix_categorie) - 1]
    questions = charger_questions(categorie)
    if not questions:
        print("Aucune question disponible. Fin du programme.")
        return
    print("\nVous avez 30 secondes par question. Bonne chance !")
    score = passer_test(questions)
    print(f"\nScore final : {score}/{len(questions)}")
    enregistrer_resultat(users, identifiant, score)
    print("\nHistorique mis à jour 😊")
    for i, test in enumerate(users[identifiant]["historique"], 1):
        print(f"{i}. {test['date']} - Score : {test['score']}")
    exporter_resultats(users)

if __name__ == "__main__":
    main()
