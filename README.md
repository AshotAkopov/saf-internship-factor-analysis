# Stage ISFA – Factor Analysis with Python

This repository contains the work carried out during my first-year Master's internship in Econometrics and Statistics at ISFA (Université Claude Bernard Lyon 1), within the Laboratory of Actuarial and Financial Sciences (SAF).

## Objective

The aim of this internship is to explore and implement factor analysis methods in Python, by developing tools that complement existing libraries, particularly for visualization and result interpretation.

## Repository content

- `FactorAnalyz.py`: main file containing the implemented functions

## Implemented methods

### Principal Component Analysis (PCA)

The developments around PCA include:

- selection of the number of components using Horn’s parallel analysis and Velicer’s MAP test;
- extraction and structuring of results using the `pca_results` function (coordinates, contributions, cos²);
- identification of the most influential variables and individuals using `pca_top`;
- visualization tools, including a correlation circle implemented in `plot_correlation_circle` with filtering options.

### Exploratory Factor Analysis (EFA)

A theoretical study of exploratory factor analysis methods was conducted.  
The practical implementation highlighted limitations due to strong multicollinearity in the data.

The following functions were developed to analyze this issue:

- `corr_over_threshold`: identifies correlations above a given threshold;
- `calculate_vif`: computes the Variance Inflation Factor (VIF) for each variable.

## Data

The dataset consists of football players from the five major European leagues, sourced from fbref.com.

After preprocessing, the final dataset includes 1852 individuals described by 127 variables.

## Context

This work was carried out within the Laboratory of Actuarial and Financial Sciences (SAF), whose research focuses on risk analysis and management in finance and insurance.

## Author

Ashot Akopov  
Master’s Degree in Econometrics and Statistics  
ISFA – Université Claude Bernard Lyon 1

---

# Version française

## Stage ISFA – Analyse factorielle avec Python

Ce dépôt contient les travaux réalisés dans le cadre de mon stage de Master 1 en Économétrie et Statistiques à l’ISFA (Université Claude Bernard Lyon 1), au sein du Laboratoire de Sciences Actuarielles et Financières (SAF).

## Objectif

L’objectif de ce stage est d’explorer et d’implémenter des méthodes d’analyse factorielle en Python, en développant des outils complémentaires aux bibliothèques existantes, notamment pour la visualisation et l’exploitation des résultats.

## Contenu du dépôt

- `FactorAnalyz.py` : fichier principal regroupant les fonctions développées

## Méthodes implémentées

### Analyse en Composantes Principales (ACP)

Les développements autour de l’ACP portent sur :

- le choix du nombre de composantes, avec l’implémentation de l’analyse parallèle de Horn et du test MAP de Velicer ;
- l’extraction et l’organisation des résultats via la fonction `pca_results`, qui calcule les coordonnées, contributions et cos² ;
- l’identification des variables ou individus les plus influents à l’aide de la fonction `pca_top` ;
- la visualisation des résultats, notamment à travers une fonction de tracé du cercle de corrélation (`plot_correlation_circle`) permettant d’appliquer différents filtres.

### Analyse Factorielle Exploratoire (AFE)

Une étude théorique des méthodes d’analyse factorielle exploratoire a été réalisée. L’implémentation pratique a mis en évidence des limites liées à la forte multicolinéarité des données.

Les fonctions suivantes ont été développées pour analyser cette problématique :

- `corr_over_threshold` : identification des corrélations supérieures à un seuil donné ;
- `calculate_vif` : calcul du Variance Inflation Factor (VIF) pour chaque variable.

## Données

Les données utilisées concernent des joueurs de football issus des cinq grands championnats européens. Elles proviennent du site fbref.com.

Après traitement, l’échantillon final comprend 1852 individus décrits par 127 variables.

## Contexte

Ce travail a été réalisé au sein du Laboratoire de Sciences Actuarielles et Financières (SAF), dont les recherches portent sur l’analyse et la gestion des risques en finance et en assurance.

## Auteur

Ashot Akopov  
Master 1 Économétrie et Statistiques  
ISFA – Université Claude Bernard Lyon 1
