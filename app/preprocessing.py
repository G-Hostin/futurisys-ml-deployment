import pandas as pd


def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # feature engineering (le meme que dans le notebook 02)
    df["revenu_par_annee_exp"] = df["revenu_mensuel"] / (df["annee_experience_totale"] + 1)
    df["satisfaction_moyenne"] = df[
        ["satisfaction_employee_environnement", "satisfaction_employee_nature_travail",
         "satisfaction_employee_equipe", "satisfaction_employee_equilibre_pro_perso"]
    ].mean(axis=1)
    df["hs_et_bas_salaire"] = ((df["heure_supplementaires"] == 1) & (df["revenu_mensuel"] < 3000)).astype(int)
    df["ratio_anciennete_promotion"] = df["annees_dans_l_entreprise"] / (df["annees_depuis_la_derniere_promotion"] + 1)
    df["ratio_poste_entreprise"] = df["annees_dans_le_poste_actuel"] / (df["annees_dans_l_entreprise"] + 1)
    df["exp_par_age"] = df["nombre_experiences_precedentes"] / df["age"]

    # regroupement des modalites rares
    top_postes = ["Consultant", "Cadre Commercial", "Assistant de Direction", "Représentant Commercial"]
    df["poste"] = df["poste"].apply(lambda x: x if x in top_postes else "Autre")

    top_domaines = ["Infra & Cloud", "Transformation Digitale", "Marketing"]
    df["domaine_etude"] = df["domaine_etude"].apply(lambda x: x if x in top_domaines else "Autre")

    # encodage ordinal
    freq_map = {"Aucun": 0, "Occasionnel": 1, "Frequent": 2}
    df["frequence_deplacement"] = df["frequence_deplacement"].map(freq_map)

    # one-hot encoding avec les memes colonnes que le modele attend
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)

    # le modele attend exactement 38 features dans un ordre precis
    expected_cols = [
        "age", "revenu_mensuel", "nombre_experiences_precedentes", "annee_experience_totale",
        "annees_dans_l_entreprise", "annees_dans_le_poste_actuel", "nombre_participation_pee",
        "nb_formations_suivies", "distance_domicile_travail", "niveau_education",
        "frequence_deplacement", "annees_depuis_la_derniere_promotion",
        "annees_sous_responsable_actuel", "satisfaction_employee_environnement",
        "note_evaluation_precedente", "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe", "satisfaction_employee_equilibre_pro_perso",
        "note_evaluation_actuelle", "heure_supplementaires", "augementation_salaire_precedente",
        "revenu_par_annee_exp", "satisfaction_moyenne", "hs_et_bas_salaire",
        "ratio_anciennete_promotion", "ratio_poste_entreprise", "exp_par_age",
        "statut_marital_Divorcé(e)", "statut_marital_Marié(e)",
        "departement_Consulting", "departement_Ressources Humaines",
        "poste_Autre", "poste_Cadre Commercial", "poste_Consultant", "poste_Représentant Commercial",
        "domaine_etude_Infra & Cloud", "domaine_etude_Marketing", "domaine_etude_Transformation Digitale",
    ]

    # ajouter les colonnes manquantes (a 0) et remettre dans le bon ordre (compensation ohe)
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_cols]

    return df