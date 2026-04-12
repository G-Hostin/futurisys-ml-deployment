# Schema de la base de donnees

## Tables

### employees

Contient le dataset d'entrainement (1470 employes avec la variable cible `a_quitte_l_entreprise`).

### prediction_inputs

Enregistre les donnees envoyees a l'API a chaque appel de prediction. Chaque ligne correspond a un appel avec un timestamp.

### prediction_outputs

Enregistre le resultat de chaque prediction, lie a l'input correspondant via une cle etrangere.

## Relations

```
employees              prediction_inputs          prediction_outputs
+------------------+   +------------------+       +------------------+
| id (PK)          |   | id (PK)          |--1:1--| id (PK)          |
| age              |   | timestamp        |       | input_id (FK)    |
| revenu_mensuel   |   | age              |       | prediction       |
| statut_marital   |   | revenu_mensuel   |       | probability      |
| departement      |   | statut_marital   |       | risk_level       |
| poste            |   | departement      |       +------------------+
| ...              |   | poste            |
| a_quitte (0/1)   |   | ...              |
+------------------+   +------------------+
```

- **PK** = Primary Key (identifiant unique)
- **FK** = Foreign Key (cle etrangere vers prediction_inputs.id)
- La relation entre prediction_inputs et prediction_outputs est **1:1** (un input = un output)
