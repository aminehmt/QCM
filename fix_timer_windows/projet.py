import json
import os
import csv
from datetime import datetime
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(script_dir, 'users.json')
questions_file = os.path.join(script_dir, 'questions.json')


def sauvegarder_utilisateurs(users): #fct sauvegarde des infos du user
    try:
        with open(users_file, 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4)
    except IOError as e:
        print(f"Erreur lors de la sauvegarde : {e}")


def charger_questions(categorie=None):#fct chargement liste de questions
    try:
        with open(questions_file, 'r', encoding='utf-8') as file:
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


def passer_test(questions, limite_par_question=30):#pour imposer une limite de temp
    score = 0
    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{j + 1}. {option}")
        
        timer_expired_event = threading.Event()
        timer = threading.Timer(limite_par_question, limite_temps_timer, [timer_expired_event])
        timer.start()

        try:
            print(f"Vous avez {limite_par_question} secondes pour répondre.")
            reponse = input("Votre réponse (1-4) : ").strip()
            timer.cancel()

            if timer_expired_event.is_set():
                raise TimeoutError
            
            if reponse.isdigit() and int(reponse) - 1 == q['reponse']:
                print("Correct ! ✅")
                score += 1
            else:
                print(f"Incorrect ❌. La bonne réponse était : {q['options'][q['reponse']]}")
        except TimeoutError:
            print("\nTemps écoulé pour cette question. Passons à la suivante.")
    return score


def exporter_resultats(users, fichier="resultats.csv"):#exportation des resultats des users dans le fichier csv
    with open(fichier, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Identifiant", "Date", "Score"])
        for user, data in users.items():
            for test in data["historique"]:
                writer.writerow([user, test["date"], test["score"]])
    print(f"Résultats exportés dans le fichier {fichier}.")

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
                print(f"Bienvenue vous etes de retour, {identifiant} ! Voici votre historique :")
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
