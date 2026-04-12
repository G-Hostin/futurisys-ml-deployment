from fastapi.testclient import TestClient
from main import app


client = TestClient(app) # crée un faux client qui parle a app (depuis main)

VALID_EMPLOYEE = {
    "age": 35, "revenu_mensuel": 5000, "statut_marital": "Célibataire",
    "departement": "Consulting", "poste": "Consultant",
    "nombre_experiences_precedentes": 3, "annee_experience_totale": 10,
    "annees_dans_l_entreprise": 5, "annees_dans_le_poste_actuel": 3,
    "nombre_participation_pee": 1, "nb_formations_suivies": 2,
    "distance_domicile_travail": 10, "niveau_education": 3,
    "domaine_etude": "Infra & Cloud", "frequence_deplacement": "Occasionnel",
    "annees_depuis_la_derniere_promotion": 2,
    "annees_sous_responsable_actuel": 3,
    "satisfaction_employee_environnement": 3,
    "note_evaluation_precedente": 3,
    "satisfaction_employee_nature_travail": 3,
    "satisfaction_employee_equipe": 2,
    "satisfaction_employee_equilibre_pro_perso": 3,
    "note_evaluation_actuelle": 3, "heure_supplementaires": 0,
    "augementation_salaire_precedente": 15.0,
}


def test_root():
    response = client.get("/") # simule un GET sur /
    assert response.status_code == 200
    assert response.json()["message"] == "Futurisys ML API is running"


def test_predict_valid_input():
    response = client.post("/predict", json=VALID_EMPLOYEE) # simule un POSt avec du json
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert "risk_level" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1
    assert data["risk_level"] in ["faible", "modéré", "élevé"]


def test_predict_invalid_age():
    invalid = VALID_EMPLOYEE.copy()
    invalid["age"] = 10
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422


def test_predict_missing_field():
    response = client.post("/predict", json={"age": 35})
    assert response.status_code == 422


def test_predict_empty_body():
    response = client.post("/predict", json={})
    assert response.status_code == 422