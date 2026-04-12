import pytest
from pydantic import ValidationError
from app.schemas import EmployeeInput


def test_valid_input():
    data = {
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
    employee = EmployeeInput(**data)
    assert employee.age == 35 # vérifie que les données sont valides et accessibles


def test_age_too_low():
    data = {
        "age": 10, "revenu_mensuel": 5000, "statut_marital": "Célibataire",
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
    with pytest.raises(ValidationError): # le code suivant doit lever une erreur ValidationError
        EmployeeInput(**data) # Pydantic plante en essayant de créer l'objet ? Age en dessous de ge=18


def test_missing_field():
    data = {"age": 35, "revenu_mensuel": 5000}
    with pytest.raises(ValidationError):
        EmployeeInput(**data) # il manque 23 champs


def test_wrong_type():
    data = {
        "age": "35", "revenu_mensuel": 5000,
        "statut_marital": "Célibataire", "departement": "Consulting",
        "poste": "Consultant", "nombre_experiences_precedentes": 3,
        "annee_experience_totale": 10, "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3, "nombre_participation_pee": 1,
        "nb_formations_suivies": 2, "distance_domicile_travail": 10,
        "niveau_education": 3, "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Occasionnel",
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
    with pytest.raises(ValidationError):
        EmployeeInput(**data) # age en texte ou lieu d'entier