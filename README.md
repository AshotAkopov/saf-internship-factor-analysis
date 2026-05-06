# Factor Analysis with Python

Python tools for principal component analysis (PCA), exploratory factor analysis (EFA), and multicollinearity diagnostics.

*French version available below.*

---

## Project Overview

This project focuses on the implementation and exploration of multivariate statistical methods in Python.

The objective is to develop practical tools for:

- dimensionality reduction,
- factor analysis,
- PCA interpretation,
- visualization,
- and multicollinearity diagnostics.

The project was developed using football performance data from the five major European leagues.

---

## Repository Content

- `factor_analysis.py`  
  Main Python file containing the implemented functions.

---

## Implemented Methods

### Principal Component Analysis (PCA)

Implemented tools include:

- Horn’s parallel analysis
- Velicer’s MAP test
- PCA result extraction
- Variable and individual contributions
- cos² computation
- Correlation circle visualization
- PCA interpretation helpers

Main functions:

- `pca_results`
- `pca_top`
- `parallel_analysis`
- `velicer_map`
- `plot_correlation_circle`

---

### Exploratory Factor Analysis (EFA)

The project also explores exploratory factor analysis and multicollinearity issues.

Implemented tools:

- Correlation threshold detection
- Variance Inflation Factor (VIF)
- Correlation diagnostics

Main functions:

- `corr_over_threshold`
- `calculate_vif`

---

## Data

The dataset contains football players from the five major European leagues, collected from fbref.com.

After preprocessing:

- 1852 observations
- 127 variables

---

## Technologies

- Python
- pandas
- numpy
- matplotlib
- scikit-learn
- statsmodels

---

## Context

This project was developed during an internship at the Laboratory of Actuarial and Financial Sciences (SAF), as part of a Master's degree in Econometrics and Statistics at ISFA — Université Claude Bernard Lyon 1.

The work focused on the implementation and exploration of multivariate statistical methods in Python, with an emphasis on PCA interpretation, factor analysis, and multicollinearity diagnostics.

---

## Author

Ashot Akopov

Master’s Degree in Econometrics and Statistics  
ISFA — Université Claude Bernard Lyon 1

---

# Version française

## Analyse factorielle avec Python

Outils Python pour l’analyse en composantes principales (ACP), l’analyse factorielle exploratoire (AFE) et les diagnostics de multicolinéarité.

---

## Présentation du projet

Ce projet porte sur l’implémentation et l’exploration de méthodes statistiques multivariées en Python.

L’objectif est de développer des outils pratiques pour :

- la réduction de dimension,
- l’analyse factorielle,
- l’interprétation des ACP,
- la visualisation,
- et les diagnostics de multicolinéarité.

Le projet a été développé à partir de données de performance de joueurs de football issus des cinq grands championnats européens.

---

## Contenu du dépôt

- `factor_analysis.py`  
  Fichier principal contenant les fonctions développées.

---

## Méthodes implémentées

### Analyse en Composantes Principales (ACP)

Outils implémentés :

- Analyse parallèle de Horn
- Test MAP de Velicer
- Extraction des résultats d’ACP
- Contributions des variables et individus
- Calcul des cos²
- Cercle des corrélations
- Outils d’interprétation des ACP

Fonctions principales :

- `pca_results`
- `pca_top`
- `parallel_analysis`
- `velicer_map`
- `plot_correlation_circle`

---

### Analyse Factorielle Exploratoire (AFE)

Le projet explore également l’analyse factorielle exploratoire et les problèmes de multicolinéarité.

Outils implémentés :

- Détection de corrélations élevées
- Variance Inflation Factor (VIF)
- Diagnostics de corrélation

Fonctions principales :

- `corr_over_threshold`
- `calculate_vif`

---

## Données

Les données concernent des joueurs des cinq grands championnats européens, collectées depuis fbref.com.

Après prétraitement :

- 1852 observations
- 127 variables

---

## Technologies

- Python
- pandas
- numpy
- matplotlib
- scikit-learn
- statsmodels

---

## Contexte

Ce projet a été réalisé dans le cadre d’un stage au Laboratoire de Sciences Actuarielles et Financières (SAF), au sein du Master Économétrie et Statistiques de l’ISFA — Université Claude Bernard Lyon 1.

Le travail porte sur l’implémentation et l’exploration de méthodes statistiques multivariées en Python, avec un intérêt particulier pour l’interprétation des ACP, l’analyse factorielle et les diagnostics de multicolinéarité.

---

## Auteur

Ashot Akopov

Master Économétrie et Statistiques  
ISFA — Université Claude Bernard Lyon 1
