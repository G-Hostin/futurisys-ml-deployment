---
title: Futurisys ML Deployment
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Futurisys ML Deployment

API de prédiction d'attrition des employés pour Futurisys, développée avec FastAPI et déployée sur Hugging Face Spaces.

## Contexte

Ce projet est un Proof of Concept (POC) réalisé pour Futurisys. L'objectif est de rendre opérationnel un modèle de machine learning capable de prédire si un employé risque de quitter l'entreprise, en l'exposant via une API REST.

Le modèle (XGBoost) a été entraîné sur un dataset de 1470 employés (dans le cadre du P4 OpenClassrooms). Il atteint un recall de 0.68 sur la classe positive (départ), ce qui signifie qu'il détecte environ 2 départs sur 3. Le F1-score correspondant est de 0.55.

## Stack technique

- **Langage** : Python 3.13
- **API** : FastAPI
- **Modèle ML** : XGBoost (classification binaire, seuil optimisé à 0.545)
- **Base de données** : PostgreSQL (local) / SQLite (CI et déploiement)
- **ORM** : SQLAlchemy
- **Validation** : Pydantic
- **CI/CD** : GitHub Actions
- **Déploiement** : Hugging Face Spaces (Docker)
- **Gestion de projet** : uv + pyproject.toml

## Installation

### Prérequis

- Python 3.13
- uv (gestionnaire de paquets)
- PostgreSQL (optionnel, SQLite est utilisé par défaut)

### Mise en place

```bash
# cloner le repo
git clone https://github.com/G-Hostin/futurisys-ml-deployment.git
cd futurisys-ml-deployment

# installer les dépendances
uv sync

# configurer la base de données (optionnel, pour PostgreSQL)
# créer un fichier .env à la racine :
# DATABASE_URL=postgresql://postgres:motdepasse@localhost:5432/futurisys

# créer les tables et insérer le dataset
uv run python -m db.create_db
```

## Utilisation

### Lancer l'API en local

```bash
uv run uvicorn main:app --reload
```

L'API est disponible sur `http://127.0.0.1:8000`.
La documentation Swagger est accessible sur `http://127.0.0.1:8000/docs`.

### Exemple d'appel

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "revenu_mensuel": 5000,
    "statut_marital": "Célibataire",
    "departement": "Consulting",
    "poste": "Consultant",
    "nombre_experiences_precedentes": 3,
    "annee_experience_totale": 10,
    "annees_dans_l_entreprise": 5,
    "annees_dans_le_poste_actuel": 3,
    "nombre_participation_pee": 1,
    "nb_formations_suivies": 2,
    "distance_domicile_travail": 10,
    "niveau_education": 3,
    "domaine_etude": "Infra & Cloud",
    "frequence_deplacement": "Occasionnel",
    "annees_depuis_la_derniere_promotion": 2,
    "annees_sous_responsable_actuel": 3,
    "satisfaction_employee_environnement": 3,
    "note_evaluation_precedente": 3,
    "satisfaction_employee_nature_travail": 3,
    "satisfaction_employee_equipe": 2,
    "satisfaction_employee_equilibre_pro_perso": 3,
    "note_evaluation_actuelle": 3,
    "heure_supplementaires": 0,
    "augementation_salaire_precedente": 15.0
  }'
```

### Réponse

```json
{
  "prediction": 0,
  "probability": 0.168,
  "risk_level": "faible"
}
```

- `prediction` : 0 = reste, 1 = quitte
- `probability` : probabilité de départ (entre 0 et 1)
- `risk_level` : faible (< 0.3), modéré (0.3 - 0.545), élevé (>= 0.545)

## API en production

L'API est déployée sur Hugging Face Spaces :
`https://g-hostin-futurisys-ml-deployment.hf.space`

Documentation Swagger en production :
`https://g-hostin-futurisys-ml-deployment.hf.space/docs`

## Structure du projet

```
futurisys-ml-deployment/
├── .github/workflows/     # pipelines CI/CD
│   ├── ci.yml             # tests + linting (push et PR)
│   └── deploy.yml         # déploiement HF Spaces (merge main)
├── app/                   # code de l'API
│   ├── preprocessing.py   # pipeline de preprocessing
│   └── schemas.py         # schémas Pydantic (validation)
├── db/                    # base de données
│   ├── database.py        # connexion SQLAlchemy
│   ├── models.py          # définition des tables
│   ├── create_db.py       # création des tables + insertion dataset
│   └── df_central.csv     # dataset d'entraînement
├── docs/                  # documentation complémentaire
│   ├── schema_db.md       # schéma de la base de données
│   └── model_doc.md       # documentation technique du modèle
├── model/                 # modèle sérialisé
│   └── model_xgb.joblib   # modèle XGBoost entraîné
├── tests/                 # tests unitaires et fonctionnels
│   ├── test_api.py        # tests des endpoints (fonctionnel)
│   ├── test_model.py      # tests du modèle (unitaire)
│   ├── test_preprocessing.py  # tests du preprocessing (unitaire)
│   └── test_schemas.py    # tests de validation Pydantic (unitaire)
├── main.py                # point d'entrée de l'API
├── Dockerfile             # configuration Docker pour HF Spaces
├── pyproject.toml         # dépendances et configuration
└── README.md
```

## Tests

```bash
# lancer les tests
uv run pytest tests/ -v

# lancer les tests avec couverture
uv run pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
```

18 tests, 97% de couverture :

**Preprocessing (4 tests unitaires)** : vérifie que le preprocessing retourne bien 38 colonnes, que le résultat est un DataFrame, qu'un poste inconnu (ex: "Data Engineer") est correctement regroupé dans la catégorie "Autre", et que la satisfaction moyenne est bien calculée à partir des 4 scores.

**Validation Pydantic (4 tests unitaires)** : vérifie que des données valides sont acceptées, qu'un âge en dessous de 18 ans est refusé, que l'envoi de données incomplètes déclenche une erreur, et qu'un type incorrect (texte au lieu d'un nombre) est rejeté.

**Modèle (5 tests unitaires)** : vérifie que le fichier joblib se charge correctement, que predict_proba retourne bien 2 probabilités (une par classe), que ces probabilités additionnées sont égales à 1.0, qu'elles sont entre 0 et 1, et qu'un profil à risque (bas salaire, heures supplémentaires, satisfaction faible, nouvel arrivant) obtient bien une probabilité de départ élevée.

**API (5 tests fonctionnels)** : vérifie que l'endpoint GET / retourne le message de statut, que POST /predict avec des données valides retourne une prédiction complète (prediction, probability, risk_level dans les bonnes bornes), et que les requêtes invalides (âge hors limites, champs manquants, body vide) retournent bien une erreur 422.

## CI/CD

**CI (ci.yml)** : se déclenche sur chaque push (dev, feature/\*) et chaque PR (dev, main). Lance le linting avec ruff puis exécute les 18 tests. Si un test échoue, la PR ne peut pas être mergée.

**CD (deploy.yml)** : se déclenche à chaque merge dans main. Envoie l'ensemble des fichiers du repo vers Hugging Face Spaces via le CLI `hf`. HF construit ensuite l'image Docker et lance l'API automatiquement.

## Base de données

Trois tables (voir docs/schema_db.md pour le schéma complet) :

- `employees` : le dataset d'entraînement (1470 employés avec la variable cible a_quitte_l_entreprise)
- `prediction_inputs` : les données envoyées à chaque appel de l'API, avec un timestamp
- `prediction_outputs` : le résultat de chaque prédiction (prediction, probability, risk_level), relié à l'input correspondant par une clé étrangère (input_id)

En local, PostgreSQL est utilisé (configuré via le fichier .env). En CI et en déploiement, SQLite est utilisé comme fallback car PostgreSQL n'est pas disponible dans ces environnements.
