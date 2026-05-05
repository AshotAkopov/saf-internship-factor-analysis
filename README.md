# Stage ISFA – Analyse factorielle avec Python

Ce dépôt contient les travaux réalisés dans le cadre de mon stage de Master 1 
en Économétrie et Statistiques à l’ISFA (Université Lyon 1), au sein du 
Laboratoire de Sciences Actuarielles et Financières (SAF).

## 🎯 Objectif du projet

L’objectif du stage est d’explorer et d’implémenter des méthodes d’analyse 
factorielle en Python, en développant des outils complémentaires aux 
bibliothèques existantes, notamment pour la visualisation et l’exploitation 
des résultats.

## 📂 Contenu du dépôt

- `FactorAnalyz.py` : fichier principal contenant les fonctions développées

## 🔬 Méthodes implémentées

### Analyse en Composantes Principales (ACP)

- **Choix du nombre de composantes**
  - Analyse parallèle de Horn
  - Test MAP de Velicer

- **Extraction des résultats**
  - `pca_results` : calcule les coordonnées, contributions et cos²
  - `pca_top` : identifie les variables ou individus les plus influents

- **Visualisation**
  - `plot_correlation_circle` : cercle de corrélation avec filtres

### Analyse Factorielle Exploratoire (AFE)

- Étude théorique des méthodes
- Analyse des limites liées à la multicolinéarité

Fonctions associées :

- `corr_over_threshold` : identifie les corrélations élevées
- `calculate_vif` : calcule le Variance Inflation Factor (VIF)

## 📊 Données

- Données de football issues des cinq grands championnats européens
- Source : fbref.com
- Échantillon final :
  - 1852 joueurs
  - 127 variables

## 📌 Contexte

Stage réalisé au laboratoire SAF, spécialisé dans l’étude des risques 
financiers et actuariels.

## 👤 Auteur

Ashot Akopov  
Master 1 Économétrie et Statistiques  
ISFA – Université Lyon 1
