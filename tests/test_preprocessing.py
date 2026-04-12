import pandas as pd
from app.preprocessing import preprocess_input


def test_output_has_38_columns():
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
    result = preprocess_input(data)
    assert result.shape[1] == 38 # le preprocess doit retourner 38 cols


def test_output_is_dataframe():
    data = {
        "age": 40, "revenu_mensuel": 3000, "statut_marital": "Marié(e)",
        "departement": "Ressources Humaines", "poste": "Autre",
        "nombre_experiences_precedentes": 5, "annee_experience_totale": 12,
        "annees_dans_l_entreprise": 8, "annees_dans_le_poste_actuel": 4,
        "nombre_participation_pee": 2, "nb_formations_suivies": 1,
        "distance_domicile_travail": 5, "niveau_education": 2,
        "domaine_etude": "Marketing", "frequence_deplacement": "Frequent",
        "annees_depuis_la_derniere_promotion": 1,
        "annees_sous_responsable_actuel": 2,
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 2,
        "note_evaluation_actuelle": 4, "heure_supplementaires": 1,
        "augementation_salaire_precedente": 20.0,
    }
    result = preprocess_input(data)
    assert isinstance(result, pd.DataFrame) # result doit être un pd.DataFrame


def test_unknown_poste_becomes_autre():
    data = {
        "age": 30, "revenu_mensuel": 4000, "statut_marital": "Divorcé(e)",
        "departement": "Commercial", "poste": "Data Engineer",
        "nombre_experiences_precedentes": 2, "annee_experience_totale": 6,
        "annees_dans_l_entreprise": 3, "annees_dans_le_poste_actuel": 1,
        "nombre_participation_pee": 0, "nb_formations_suivies": 3,
        "distance_domicile_travail": 15, "niveau_education": 4,
        "domaine_etude": "Autre", "frequence_deplacement": "Aucun",
        "annees_depuis_la_derniere_promotion": 0,
        "annees_sous_responsable_actuel": 1,
        "satisfaction_employee_environnement": 1,
        "note_evaluation_precedente": 4,
        "satisfaction_employee_nature_travail": 2,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "note_evaluation_actuelle": 2, "heure_supplementaires": 1,
        "augementation_salaire_precedente": 11.0,
    }
    result = preprocess_input(data) # on envoie "poste": "Data Engineer" qui n'existe pas dans les données de base
    assert result["poste_Autre"].iloc[0] == 1 # après le ohe, Autre doit valoir 1 si le poste a bien été mis dans autre


def test_feature_engineering_satisfaction_moyenne():
    data = {
        "age": 28, "revenu_mensuel": 2500, "statut_marital": "Célibataire",
        "departement": "Consulting", "poste": "Consultant",
        "nombre_experiences_precedentes": 1, "annee_experience_totale": 4,
        "annees_dans_l_entreprise": 2, "annees_dans_le_poste_actuel": 1,
        "nombre_participation_pee": 0, "nb_formations_suivies": 1,
        "distance_domicile_travail": 3, "niveau_education": 3,
        "domaine_etude": "Transformation Digitale",
        "frequence_deplacement": "Occasionnel",
        "annees_depuis_la_derniere_promotion": 1,
        "annees_sous_responsable_actuel": 2,
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 2,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 2,
        "note_evaluation_actuelle": 3, "heure_supplementaires": 0,
        "augementation_salaire_precedente": 13.0,
    }
    result = preprocess_input(data)
    expected = (4 + 2 + 4 + 2) / 4  # donc on attend 3
    assert result["satisfaction_moyenne"].iloc[0] == expected # on vérifie si le calcul est bon