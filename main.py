from fastapi import FastAPI
import csv

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
def get_questions(use: str = None, subject: str = None):
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

    return filtered_questions
