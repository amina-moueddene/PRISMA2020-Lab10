# Lab 10 : Rédiger et valider une revue systématique selon PRISMA 2020

[![PRISMA 2020](https://img.shields.io/badge/Standard-PRISMA%202020%20(27%20items)-blue.svg)](#4-conformité-prisma-2020-et-audit-automatisé)
[![Audit](https://img.shields.io/badge/Coherence%20Audit-44%2F44%20VALIDATED-brightgreen.svg)](#4-conformité-prisma-2020-et-audit-automatisé)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](#2-prérequis-et-installation)
[![LaTeX](https://img.shields.io/badge/LaTeX-elsarticle-orange.svg)](#5-compilation-du-manuscrit)

**Titre du manuscrit :** *Machine learning and remote sensing for disease and stress detection in olive (Olea europaea L.): a systematic review of platforms, targets, algorithms and validation practice*  
**Auteure :** Amina Moueddene  
**Bases de données :** Scopus et Web of Science Core Collection (recherche exécutée le 15 novembre 2026, période couverte : 2013–2026)  
**Corpus final inclus :** 22 études distinctes (23 rapports publiés : 19 articles de revue et 3 actes de conférence)

---

## 1. Contexte scientifique et Questions de Recherche (RQ1–RQ5)

Cette revue systématique synthétise les avancées méthodologiques et opérationnelles de l'apprentissage automatique (*Machine Learning* et *Deep Learning*) couplé à la télédétection pour la détection précoce des maladies et stress abiotiques de l'olivier (*Olea europaea* L.).

Le protocole suit intégralement les directives **PRISMA 2020** (Page et al., 2021) et répond à cinq questions de recherche structurantes :
* **RQ1 (Évolution spatio-temporelle) :** Comment la production scientifique sur la détection des maladies et stress de l'olivier par télédétection et IA a-t-elle évolué entre 2013 et 2026, et quelle est sa répartition géographique ?
* **RQ2 (Plateformes et capteurs) :** Quelles plateformes d'acquisition (satellite, drone/UAV, avion) et quels types de capteurs (multispectral, hyperspectral, RGB, multimodal) sont privilégiés selon les cibles phytosanitaires ?
* **RQ3 (Cibles pathologiques et stress) :** Quels agents pathogènes (ex. *Xylella fastidiosa*, *Verticillium dahliae*, *Spilocaea oleagina*) et stress (hydrique, nutritionnel) sont étudiés, et quelles sont les associations statistiques entre plateformes et cibles ?
* **RQ4 (Algorithmes et performances) :** Quelles familles d'algorithmes (ML classique vs Deep Learning) sont employées et comment leurs performances rapportées varient-elles selon la rigueur de validation ?
* **RQ5 (Validation, qualité et maturité opérationnelle) :** Quel est le niveau de qualité méthodologique (scores `Q1–Q10`), de rigueur de validation (`V0–V5`) et de maturité de déploiement (`DRL1–DRL5`) des modèles publiés ?

---

## 2. Prérequis et installation

### Environnement logiciel et pile technologique
* **Python ≥ 3.10** (pile scientifique utilisée pour l'audit de cohérence, les tests statistiques inférentiels et la génération des figures haute résolution à 300 dpi).
* **Distribution LaTeX** (`pdflatex` + `bibtex`, TeX Live ou Overleaf) pour la compilation du manuscrit au format Elsevier (`elsarticle`).
* **Pandoc** (optionnel) pour la synchronisation automatique de la version Markdown du manuscrit.

### Installation des dépendances Python
```bash
git clone https://github.com/amina-moueddene/PRISMA2020-Lab10.git
cd PRISMA2020-Lab10
python3 -m venv .venv
source .venv/bin/activate        # Sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Architecture complète du dépôt

```text
PRISMA2020-Lab10-main/
├── README.md                                 # Documentation principale et guide de reproductibilité
├── requirements.txt                          # Dépendances Python exactes (pandas, numpy, scipy, matplotlib, seaborn, pypdf)
├── .github/
│   └── workflows/
│       └── validate.yml                      # Intégration continue (audit PRISMA + régénération figures + tests unitaires)
├── manuscript/
│   ├── systematic_review_prisma2020.tex      # Manuscrit complet en 9 sections (format elsarticle, anglais)
│   ├── refs_included.bib                     # Bibliographie BibTeX (23 rapports inclus + références méthodologiques)
│   ├── systematic_review_prisma2020.pdf      # Version PDF compilée prête à la relecture (64 pages)
│   └── systematic_review_prisma2020.md       # Copie Markdown synchronisée lisible directement sur GitHub
├── figures/                                  # 6 figures vectorielles (PDF) et haute résolution raster (PNG, 300 dpi)
│   ├── Fig1_PRISMA_flow.{pdf,png}            # Diagramme de flux PRISMA 2020 (identification → inclusion)
│   ├── Fig2_years_countries.{pdf,png}        # Distribution temporelle (2013–2026) et géographique par plateforme
│   ├── Fig3_platform_target.{pdf,png}        # Matrice Plateforme × Cible et résidus ajustés de Pearson
│   ├── Fig4_performance_vs_validation.{pdf,png} # Relation entre métriques rapportées et niveau de validation
│   ├── Fig5_quality_heatmap.{pdf,png}        # Carte thermique de l'évaluation qualité (critères Q1–Q10)
│   └── Fig6_validation_deployment.{pdf,png}  # Profils de maturité de validation (V0–V5) et déploiement (DRL1–5)
├── supplementary/
│   ├── S1_screening_ledger.csv               # Journal complet du tri titres/résumés (n = 143 notices, κ = 0,70)
│   ├── S2_fulltext_eligibility.csv           # Évaluation d'éligibilité des textes intégraux (n = 53 recherchés, 38 évalués)
│   ├── S3_fulltext_extraction_22_studies.csv # Grille d'extraction détaillée des 22 études incluses
│   ├── S4_quality_assessment_Q1-Q10.csv      # Notation méthodologique Q1–Q10 (/20 points) par étude
│   ├── S5_studies_master_v2.csv              # Table maître codée (plateformes, capteurs, V0–V5, DRL1–5, performances)
│   ├── lab8_consolidated_extraction_qa.csv   # Fusion consolidée extraction + qualité (issu du Lab 8)
│   ├── tableau_comparatif.csv                # Synthèse comparative des 22 études (issu du Lab 9)
│   ├── statistiques_performances.csv         # Statistiques descriptives et inférentielles par famille d'algorithmes
│   ├── limitations_frequentes.csv            # Taxonomie des biais et limites méthodologiques récurrentes
│   ├── potential_gaps.csv                    # Cartographie des lacunes de recherche (Research Gaps)
│   ├── synthese_lab9.json                    # Agrégats quantitatifs structurés de la synthèse
│   ├── checklist_prisma2020_27items.md       # Checklist officielle PRISMA 2020 complétée (27 items et sous-items)
│   ├── verification_finale_lab10.md          # Rapport de validation finale, réponses Q1–Q5 et Défis 1–2
│   └── validation_coherence_lab10.json       # Sortie JSON horodatée de l'audit automatique (44/44 contrôles)
├── scripts/
│   ├── generate_figures.py                   # Régénération reproductible à 300 dpi des 6 figures (PDF + PNG) depuis S1–S5
│   ├── validate_manuscript_coherence.py      # Audit automatisé texte ↔ données CSV ↔ figures (44 vérifications)
│   ├── build_manuscript.sh                   # Script de compilation LaTeX (pdflatex + bibtex)
│   ├── tex_to_markdown.py                    # Synchronisation du manuscrit .tex vers .md
│   └── latex_preview/                        # Classe de repli elsarticle pour compilation locale autonome
└── tests/
    └── test_lab10.py                         # Suite de tests unitaires (livrables, S1–S5, figures 300 dpi, audit, checklist)
```

---

## 4. Conformité PRISMA 2020 et audit automatisé

Le dépôt intègre trois mécanismes garantissant la traçabilité et la reproductibilité demandées par PRISMA 2020 :

1. **Checklist officielle PRISMA 2020 (`supplementary/checklist_prisma2020_27items.md`) :** chaque item (1 à 27, incluant les sous-items `10a/10b`, `13a–13f`, `16a/16b`, `20a–20d`, `23a–23d`, `24a–24c`) est renseigné avec le numéro de section et de page exact dans le manuscrit.
2. **Audit de cohérence automatisé (`scripts/validate_manuscript_coherence.py`) :** exécute **44 contrôles croisés** entre le fichier `.tex`, les tables `S1`–`S5`, le fichier `.bib` et le dossier `figures/` :
   * Vérification de la présence des **9 sections obligatoires** et du titre (< 15 mots).
   * Recalcul indépendant de tous les effectifs du diagramme de flux PRISMA (`215 → 72 doublons → 143 → 53 → 38 → 23 rapports / 22 études`).
   * Vérification de la concordance des statistiques inférentielles ($\chi^2$, $V$ de Cramér, corrélation de Spearman $\rho$, médiane et IQR des scores QA).
   * Contrôle d'intégrité des citations BibTeX et de l'existence de toutes les figures référencées.
3. **Reproductibilité graphique (`scripts/generate_figures.py`) :** régénère à la demande les 6 figures analytiques (`Fig1`–`Fig6`) en formats vectoriel (`PDF`) et haute résolution (`PNG`, `300 dpi`) directement à partir des fichiers `S1`–`S5`.

### Exécution des scripts de validation, de génération et des tests
```bash
# 1. Exécuter l'audit complet de cohérence (44 vérifications)
python3 scripts/validate_manuscript_coherence.py

# 2. Régénérer les 6 figures haute résolution (300 dpi) depuis S1–S5
python3 scripts/generate_figures.py --output-dir figures

# 3. Lancer la suite complète de tests unitaires
python3 -m unittest discover -s tests -v
```

---

## 5. Compilation du manuscrit

* **Sur Overleaf (recommandé pour soumission Elsevier) :** importer les dossiers `manuscript/` et `figures/` dans un même projet Overleaf en conservant la structure relative (`\graphicspath{{../}}` dans `systematic_review_prisma2020.tex`) et compiler avec `pdfLaTeX`.
* **En local :** exécuter `bash scripts/build_manuscript.sh`. Le script détecte automatiquement si `elsarticle.cls` est installé sur le système et bascule sinon sur `scripts/latex_preview/` afin de garantir une compilation PDF identique en pagination (64 pages).

---

## 6. Synthèse des résultats clés

| Dimension | Résultats vérifiés depuis `S1`–`S5` |
| :--- | :--- |
| **Flux PRISMA 2020** | **215** notices identifiées (Scopus : 118 ; WoS : 97) $\rightarrow$ **72** doublons retirés $\rightarrow$ **143** notices examinées ($\kappa = 0,70$, concordance $124/143$) $\rightarrow$ **53** rapports recherchés $\rightarrow$ **15** non obtenus $\rightarrow$ **38** textes intégraux évalués $\rightarrow$ **15** exclus $\rightarrow$ **23** rapports (**22** études uniques) inclus. |
| **Plateformes & Capteurs** | **Plateformes :** Satellite ($n = 10$), UAV ($n = 7$), Avion ($n = 5$). **Capteurs :** Multispectral ($n = 11$), Multimodal ($n = 6$), RGB ($n = 3$), Hyperspectral ($n = 2$). |
| **Cibles phytosanitaires** | Pathogènes vasculaires ($n = 11$, dont *Xylella fastidiosa* et *Verticillium dahliae*), stress hydrique ($n = 7$), pathogènes foliaires ($n = 2$), cibles mixtes ($n = 2$). Association plateforme $\times$ cible significative : $\chi^2 = 17,7$, $p = 0,002$, $V = 0,63$ (scénario A) et $V = 0,51$ (scénario B). |
| **Algorithmes & Validation** | **Modèles :** ML classique ($n = 18$) vs Deep Learning ($n = 4$). **Niveaux de validation :** V0 ($1$), V1 ($2$), V2 ($8$), V3 ($8$), V4 ($3$), V5 ($0$). **Maturité :** DRL2 ($11$), DRL3 ($8$), DRL4 ($3$). |
| **Qualité & Biais** | Score QA médian : **10,5 / 20** (IQR : $9\text{–}14$). Corrélation négative forte entre précision rapportée et rigueur de validation ($\rho = -0,70$), mettant en évidence une inflation optimiste des performances en l'absence de validation spatio-temporelle indépendante. |
