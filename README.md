# Titre : 
Machine learning et télédétection pour la détection des maladies et du stress de l'olivier (Olea europaea L.) : une revue systématique des plateformes, cibles, algorithmes et pratiques de validation.

# Abstract (Résumé Structuré)
* **Objectif :** Cette revue systématique évalue l'utilisation du Machine Learning (ML) appliqué à l'imagerie par satellite, avion et drone (UAV) pour la détection des maladies (notamment *Xylella fastidiosa* et *Verticillium dahliae*) et du stress hydrique chez l'olivier, en analysant la fiabilité des méthodes de validation.
* **Méthodes :** Conformément aux lignes directrices PRISMA 2020, nous avons interrogé Scopus et Web of Science Core Collection (2013-2026). Sur 215 articles identifiés, 143 uniques ont été criblés. Après filtrage sur titre/résumé puis évaluation du texte intégral, 22 études primaires (23 rapports) ont été incluses.
* **Résultats :** Une forte association existe entre la plateforme et la cible. L'imagerie aéroportée hyperspectrale/thermique est utilisée pour les pathogènes vasculaires (11 études), tandis que les satellites multispectraux ciblent majoritairement le stress hydrique (7 études). Le DL est confiné à l'imagerie RGB par UAV pour les symptômes foliaires visibles. Les taux de précision rapportés sont souvent très élevés (médiane > 90% pour les splits internes), mais chutent drastiquement lors des 3 seuls tests de transfert géographique ou temporel identifiés.
* **Conclusion :** Bien que prometteuses, les solutions actuelles souffrent de validations surestimées par des fuites de données (data leakage) et d'une incapacité à distinguer l'infection vasculaire du déficit hydrique. Des protocoles de validation externes rigoureux sont nécessaires avant tout déploiement opérationnel.

---

# 1. Introduction
* **Contexte :** L'oléiculture, concentrée dans le bassin méditerranéen, est gravement menacée par des pathogènes vasculaires (comme *Xylella fastidiosa* et *Verticillium dahliae*) et par l'augmentation des épisodes de sécheresse. L'imagerie aérienne couplée à l'IA offre une solution non destructive de surveillance à grande échelle.
* **Problématique :** De nombreuses études annoncent des taux de précision très élevés. Cependant, les algorithmes de Machine Learning sont sensibles aux fuites de données (data leakage), et les symptômes physiques du déficit hydrique miment souvent ceux de l'infection vasculaire (fermeture stomatique).
* **Objectifs :** (RQ1) Identifier les cibles et références. (RQ2) Analyser les capteurs et plateformes utilisés. (RQ3) Identifier les méthodes d'IA. (RQ4) Évaluer la rigueur des protocoles de validation et le risque de biais. (RQ5) Évaluer le niveau de préparation au déploiement (DRL).

---

# 2. Méthodes
* **Protocole :** Revue systématique réalisée selon PRISMA 2020. *(Note d'édition : insérer ici la mention de l'enregistrement PROSPERO/OSF si applicable).*
* **Sources :** Scopus (TITLE-ABS-KEY) et Web of Science Core Collection (TS). Recherche effectuée le 15 novembre 2026 pour la période 2013-2026.
* **Search Strings :** Équation en 4 blocs (culture AND plateforme AND cible AND méthode) documentée dans les *Supplementary Materials*.
* **Sélection :** Déduplication par DOI normalisé (70 retirés) et titre (2 retirés). Screening assisté par IA générative avec vérification manuelle complète (Accord relecture en aveugle : 86,7%, $\kappa$ = 0,70).
* **Extraction et Qualité :** Grille d'extraction ciblant le contexte, les capteurs, les méthodes ML/DL, la validation (V0-V5) et le déploiement (DRL1-5). Évaluation de la qualité sur 10 critères (Q1-Q10).

---

# 3. Résultats
## 3.1. Sélection des études (Flux PRISMA)
* Identifiés : 215 (Scopus 118, WoS 97).
* Uniques après déduplication : 143.
* Exclus sur Titre/Résumé : 90 (dont 36 hors-sujet végétal, 17 sans stress ciblé).
* Non retrouvés : 15.
* Évalués en texte intégral : 38.
* Exclus en texte intégral : 15 (dont 5 sans modèle d'apprentissage).
* **Inclus finaux :** 22 études primaires (via 23 rapports).

## 3.2. Caractéristiques par RQ (Sélection)
* **RQ2 (Plateformes) :** Satellites (10), UAV (7), Aéroportés (5).
* **RQ1/RQ3 (Cibles et Méthodes) :** Pathogènes vasculaires (11), Stress hydrique (7). Le ML classique est dominant (18/22). Le Deep Learning (4/22) est exclusivement utilisé avec des drones (UAV) sur des images RGB.
* **RQ4 (Validation) :** La majorité des études ne dépassent pas la validation interne (V1: 2 études, V2: 8 études, V3: 8 études). Seulement 3 études atteignent le niveau V4 (Test de transfert explicite). Le score de qualité (QA) médian est de 10,5/20.

---

# 4. Discussion : Tendances, Limitations et Gaps
* **Tendances :** Spécialisation des plateformes : hyperspectral aéroporté pour la maladie vasculaire, satellite pour le stress hydrique, drone RGB pour les symptômes foliaires.
* **Limitations des études :** Forte suspicion de *Data Leakage* (14 études sur 22, ex: pixels voisins dans le train/test split). Vérité terrain souvent faible pour le DL (pas de tests qPCR).
* **Research Gaps :** 
  1. *Spécificité du signal :* Aucune étude n'a utilisé un plan factoriel pour séparer l'infection pathogène du simple déficit hydrique.
  2. *Validation externe :* Les modèles s'effondrent lors des transferts géographiques inter-zones (ex: rappel chutant à 10% dans l'étude D'Addabbo et al. 2025).

---

# 5. Limitations de la Revue
La revue a été menée principalement par un seul relecteur (avec un audit en aveugle $\kappa=0,70$), ce qui dévie du standard PRISMA à double relecture indépendante. De plus, 15 rapports n'ont pu être récupérés en texte intégral. Des bases importantes en ingénierie comme IEEE Xplore n'ont pas été incluses dans le flux principal.

---

# 6. Conclusion
Le ML couplé à la télédétection offre un potentiel immense pour la surveillance de l'olivier. Cependant, la fiabilité clinique des modèles actuels est largement surestimée par des pratiques de validation internes (splits aléatoires). Les futures recherches doivent imposer des tests de transferts inter-saisons et inter-vergers, et clarifier la distinction spectrale entre maladie vasculaire et stress hydrique avant d'envisager des applications opérationnelles.
