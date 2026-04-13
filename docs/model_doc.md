# Documentation technique du modèle

## Problématique

Prédire si un employé va quitter l'entreprise (attrition) à partir de ses données RH.
Classification binaire : 0 = reste, 1 = quitte.

## Données

- Source : 3 fichiers CSV (SIRH, évaluations, sondage) fusionnés en un dataframe central
- 1470 employés, 32 colonnes avant preprocessing
- Déséquilibre : 84% restent, 16% partent

## Preprocessing

Étapes appliquées (reproduites dans app/preprocessing.py) :

1. Suppression des colonnes constantes (nombre_heures_travaillees, nombre_employee_sous_responsabilite, ayant_enfants)
2. Suppression des colonnes non discriminantes (id_employee, genre) et fortement corrélées (niveau_hierarchique_poste)
3. Feature engineering (6 nouvelles variables) :
   - revenu_par_annee_exp : revenu mensuel / (expérience totale + 1)
   - satisfaction_moyenne : moyenne des 4 scores de satisfaction
   - hs_et_bas_salaire : flag si heures sup + salaire < 3000
   - ratio_anciennete_promotion : ancienneté / (années depuis promo + 1)
   - ratio_poste_entreprise : années dans le poste / (années dans l'entreprise + 1)
   - exp_par_age : nombre d'expériences précédentes / âge
4. Regroupement des modalités rares pour poste et domaine_etude
5. Encodage ordinal de frequence_deplacement (Aucun=0, Occasionnel=1, Frequent=2)
6. One-hot encoding des variables catégorielles restantes

Résultat : 38 features numériques.

## Modèle

- Algorithme : XGBoost (XGBClassifier)
- Optimisation : GridSearchCV avec validation croisée stratifiée (5 folds x 3 répétitions)
- Seuil de classification : 0.545 (optimisé via courbe précision-rappel, notebook 04)
- scale_pos_weight : 5.19 (compensation du déséquilibre des classes)

### Hyperparamètres optimisés

| Paramètre         | Valeur |
|-------------------|--------|
| n_estimators      | 300    |
| max_depth         | 2      |
| learning_rate     | 0.03   |
| subsample         | 0.6    |
| colsample_bytree  | 0.8    |
| min_child_weight  | 10     |
| reg_alpha         | 1.0    |
| reg_lambda        | 3.0    |
| gamma             | 0.3    |

## Performances

### Sur le jeu de test (294 employés)

|            | Précision | Recall | F1-score |
|------------|-----------|--------|----------|
| Reste (0)  | 0.93      | 0.85   | 0.89     |
| Quitte (1) | 0.46      | 0.68   | 0.55     |
| Accuracy   |           |        | 0.82     |

Dans le contexte métier, le recall est la métrique la plus importante : mieux vaut détecter un employé à risque (quitte à se tromper parfois) que de le rater. Le recall de 0.68 signifie que le modèle détecte environ 2 départs sur 3.

Le F1-score de 0.55 sur la classe positive reste raisonnable vu le déséquilibre (16% de départs seulement).

### Niveaux de risque

L'API retourne un niveau de risque basé sur la probabilité :
- Faible : probabilité < 0.3
- Modéré : 0.3 <= probabilité < 0.545
- Élevé : probabilité >= 0.545

## Sérialisation

Le modèle est sérialisé avec joblib (model/model_xgb.joblib, 272 Ko).
Il est chargé une seule fois au démarrage de l'API.

## Limites connues

- Le modèle a été entraîné sur 1470 employés d'une seule entreprise (TechNova Partners). Sa généralisation à d'autres entreprises n'est pas garantie.
- Les postes et domaines d'étude non vus à l'entraînement sont regroupés dans "Autre", ce qui peut réduire la précision pour ces cas.
- Le déséquilibre des classes (16% de départs) limite la précision sur la classe positive.

## Protocole de mise à jour

1. Collecter de nouvelles données d'employés
2. Ré-entraîner le modèle avec le même pipeline de preprocessing
3. Évaluer les performances sur un jeu de test
4. Si les performances sont satisfaisantes, sérialiser le nouveau modèle avec joblib
5. Remplacer model/model_xgb.joblib dans le repo
6. Le pipeline CI/CD déploie automatiquement la nouvelle version
