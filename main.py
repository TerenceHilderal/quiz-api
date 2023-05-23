from fastapi import FastAPI
import csv
import random

# Charger les données du fichier CSV
app = FastAPI()


def load_data_from_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data


@app.get("/questions")
def get_questions(use: str = None, subject: str = None, num_questions: int = 5):
    data = load_data_from_csv('./questions.csv')
    filtered_questions = []
    if use:
        filtered_questions = [
            question for question in data if question['use'] == use]
    elif subject:
        filtered_questions = [
            question for question in data if question['subject'] == subject]
    else:
        return {"error": "Veuillez fournir un paramètre 'use' ou 'subject'."}

    random.shuffle(filtered_questions)  # Mélange aléatoire des questions

    # Sélection du nombre de questions demandé
    selected_questions = filtered_questions[:num_questions]

    return selected_questions
