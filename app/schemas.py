from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    age: int = Field(ge=18, le=100, examples=[35])
    revenu_mensuel: int = Field(examples=[5000])
    statut_marital: str = Field(examples=["Célibataire"])
    departement: str = Field(examples=["Consulting"])
    poste: str = Field(examples=["Consultant"])
    nombre_experiences_precedentes: int = Field(ge=0, examples=[3])
    annee_experience_totale: int = Field(ge=0, examples=[10])
    annees_dans_l_entreprise: int = Field(ge=0, examples=[5])
    annees_dans_le_poste_actuel: int = Field(ge=0, examples=[3])
    nombre_participation_pee: int = Field(ge=0, examples=[1])
    nb_formations_suivies: int = Field(ge=0, examples=[2])
    distance_domicile_travail: int = Field(ge=0, examples=[10])
    niveau_education: int = Field(ge=1, le=5, examples=[3])
    domaine_etude: str = Field(examples=["Infra & Cloud"])
    frequence_deplacement: str = Field(examples=["Occasionnel"])
    annees_depuis_la_derniere_promotion: int = Field(ge=0, examples=[2])
    annees_sous_responsable_actuel: int = Field(ge=0, examples=[3])
    satisfaction_employee_environnement: int = Field(ge=1, le=4, examples=[3])
    note_evaluation_precedente: int = Field(ge=1, le=4, examples=[3])
    satisfaction_employee_nature_travail: int = Field(ge=1, le=4, examples=[3])
    satisfaction_employee_equipe: int = Field(ge=1, le=4, examples=[2])
    satisfaction_employee_equilibre_pro_perso: int = Field(ge=1, le=4, examples=[3])
    note_evaluation_actuelle: int = Field(ge=1, le=5, examples=[3])
    heure_supplementaires: int = Field(ge=0, le=1, examples=[0])
    augementation_salaire_precedente: float = Field(ge=0, examples=[15.0])


class PredictionOutput(BaseModel):
    prediction: int = Field(description="0 = reste, 1 = quitte")
    probability: float = Field(description="Probabilité de quitter l'entreprise")
    risk_level: str = Field(description="Niveau de risque: faible, modéré, élevé")