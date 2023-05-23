from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import csv
import random

# Charger les données du fichier CSV
app = FastAPI()
security = HTTPBasic()

# création model


class QuestionCreate(BaseModel):
    question: str
    subject: str
    correct: str
    use: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str

# vérifier que l'api est fonctionnelle


@app.get("/")
def check_api_status():
    return {"message": "L'API est fonctionnelle"}


def load_data_from_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data

# on récupère les questions en fonction de use de subject et du nombre de question souhaité


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


'''
PARTIE ADMIN A VOIR DEMAIN

'''


def validate_admin_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    username = "admin"
    password = "4dm1N"

    if credentials.username != username or credentials.password != password:
        raise HTTPException(
            status_code=401,
            detail="Identifiants d'administrateur invalides",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/questions")
def create_question(question: QuestionCreate, credentials: HTTPBasicCredentials = Depends(validate_admin_credentials)):
    # Logique de création de la nouvelle question ici
    return {"message": "Nouvelle question créée avec succès"}
