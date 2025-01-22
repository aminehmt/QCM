import json
import os
import csv 
from datetime import datetime
from time import time
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(script_dir, 'users.json')
questions_file = os.path.join(script_dir, 'questions.json') 

def charger_utilisateurs(): #fonction pour utilisateurs
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as file: #ouverture du fichier
            try:
                return json.load(file)
            except json.JSONDecodeError: #gestion derreur 
                print("Erreur : Le fichier users.json est corrompu. Voulez vous le reinitialiser ? (O/N)")
                choix = input().strip().lower()
                if choix == 'O':
                    return {} #reinitialisation du fichier(vide)
                else:
                    print("Fermeture de l'application.")
                    exit()
    return {}

def sauvegarder_utilisateurs(users): #fonction pour sauvegarder les utilisateurs
    try:
         with open(users_file, 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4) #ecriture des donnees
    except IOError as e: #en cas derreur
        print(f"Erreur lors de la sauvegarde : {e}")

def authentification(users):   #fonction pour la connexion
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
       
#normalement tout est clair hena
def charger_questions(categorie=None): #et had la fct pour charger les questiosn depuis un fichier questions.json
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
    #si vous avez des qst 9oloLI 

def limite_temps_timer(timer_expired_event):
    timer_expired_event.set()


def passer_test(questions, limite_par_question=30):#pour imposer une limite de temp
    score = 0
    debut = time() #pour calculer le temps total passee
    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{j + 1}. {option}")
        
        timer_expired_event = threading.Event()
        timer = threading.Timer(limite_par_question, limite_temps_timer, [timer_expired_event])
        timer.start()

        try:
            print(f"Vous avez {limite_par_question} secondes pour répondre.")
            reponse = None
            while not timer_expired_event.is_set():
                reponse = input("Votre réponse (1-4) : ").strip()
                if not reponse.isdigit() or not (1 <= int(reponse) <= 4):#gestion reponse entre 1-4 seulement
                    print("Veuillez choisir une option valide entre 1 et 4.")
                else:
                    break

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
   
    temps_total = time() - debut  # Calcul totale du test
    print(f"\nTemps total pour compléter le test : {temps_total:.2f} secondes")
    return score,temps_total

def enregistrer_resultat(users, identifiant, score, temps_total): #save resultat bch thato f fichier
    users[identifiant]["historique"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "temps_total": round(temps_total, 2)
    })
    sauvegarder_utilisateurs(users)


def exporter_resultats(users, fichier="resultats.csv"): #had la fonction t'exporti les résultats des users dans un fichiers CSV
    with open(fichier, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Identifiant", "Date", "Score","Temps_total"])
        for user, data in users.items(): #t parcouri ge3 les users ou l historique des tests
            for test in data["historique"]:
                writer.writerow([user, test["date"], test["score"],test.get("temps_total", "N/A")]) # pour chaque user tdir une ligne fel fichier avec identifiant date et score et total temp
    print(f"Résultats exportés dans le fichier {fichier}.")

def main(): # c'est la fonction principale donc tdir déroulement te3 l QCM
    users = charger_utilisateurs() #chargement des users
    identifiant = authentification(users) # authentifie user
    print("\nCatégories disponibles 😊")
    categories = set([q["categorie"] for q in charger_questions() if "categorie" in q])
    for i, cat in enumerate(categories, 1):#affiche les catégories dispo
        print(f"{i}. {cat}")
    choix_categorie = input("\nChoisissez une catégorie (ou appuyez sur Entrée pour toutes) : ")
    categorie = None
    if choix_categorie.isdigit() and 1 <= int(choix_categorie) <= len(categories):
        categorie = list(categories)[int(choix_categorie) - 1]
    questions = charger_questions(categorie) #charger les qst de la catégorie li kheyerha l user 
    if not questions:
        print("Aucune question disponible. Fin du programme.")
        return
    print("\nVous avez 30 secondes par question. Bonne chance !")
    score, temps_total = passer_test(questions)
    print(f"\nScore final : {score}/{len(questions)}")
    enregistrer_resultat(users, identifiant, score,temps_total)#enregistre le résultat du test et l historique yesralo update 
    print("\nHistorique mis à jour 😊")
    for i, test in enumerate(users[identifiant]["historique"], 1):#affichage te3 l'historique pour l user 
         print(f"{i}. {test['date']} - Score : {test['score']} - Temps : {test['temps_total']} secondes")
    exporter_resultats(users) #le resultat est exporté fel fichier CSV

if  __name__ == "__main__": # condition pour executer la fonction mais donc bch yebda l qcm et tverifier si script yet executa directement 
    main()
