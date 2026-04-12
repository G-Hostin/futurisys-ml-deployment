import pandas as pd
from db.database import engine, SessionLocal, Base
from db.models import Employee


def create_tables():
    Base.metadata.create_all(engine) # crée toutes les tables avec classe Base
    print("Tables creees avec succes")


def insert_dataset():
    df = pd.read_csv("db/df_central.csv")

    # on garde uniquement les colonnes qui correspondent a la table employees
    cols_to_drop = [
        "id_employee", "genre", "nombre_heures_travaillees",
        "nombre_employee_sous_responsabilite", "ayant_enfants",
        "niveau_hierarchique_poste",
    ]
    df = df.drop(columns=cols_to_drop)

    session = SessionLocal()
    try:
        for _, row in df.iterrows(): # parcourt le df ligne par ligne, chaque itération donne un tuple (index, row)
            employee = Employee(**row.to_dict()) # transforme la ligne en dictionnaire ({"age": 41, "revenu_mensuel": 5993, ...}) + ** qui unpack
            session.add(employee)
        session.commit()
        print(f"{len(df)} employes inseres avec succes")
    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
    finally:
        session.close()


if __name__ == "__main__": # empeche l'execution des fonction via l'im
    create_tables()
    insert_dataset()