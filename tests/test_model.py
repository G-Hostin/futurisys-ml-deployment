import joblib
import numpy as np
from app.preprocessing import preprocess_input


model = joblib.load("model/model_xgb.joblib")
THRESHOLD = 0.545

VALID_DATA = {
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


def test_model_loads():
    assert model is not None # verifie que le modele se charge correctement


def test_predict_proba_shape():
    df = preprocess_input(VALID_DATA)
    proba = model.predict_proba(df)
    assert proba.shape == (1, 2) # modèle retourne bien 2 proba


def test_predict_proba_sums_to_one():
    df = preprocess_input(VALID_DATA)
    proba = model.predict_proba(df)
    assert abs(proba[0][0] + proba[0][1] - 1.0) < 0.001 # les deux proba additionnées font bien 1 (avec arrondis)


def test_predict_proba_between_zero_and_one():
    df = preprocess_input(VALID_DATA)
    proba = model.predict_proba(df)[:, 1][0]
    assert 0 <= proba <= 1 # proba comprise entre 0 et 1



def test_high_risk_employee():
    high_risk = VALID_DATA.copy()
    high_risk["heure_supplementaires"] = 1
    high_risk["revenu_mensuel"] = 1500
    high_risk["annees_dans_l_entreprise"] = 0
    high_risk["satisfaction_employee_environnement"] = 1
    high_risk["satisfaction_employee_equipe"] = 1
    high_risk["satisfaction_employee_equilibre_pro_perso"] = 1
    high_risk["satisfaction_employee_nature_travail"] = 1
    df = preprocess_input(high_risk)
    proba = model.predict_proba(df)[:, 1][0]
    assert proba > 0.3 # verifie qu'un employe avec des signaux negatifs (bas salaire + h supp + satsif basse + nouveau) a bien une proba elevee