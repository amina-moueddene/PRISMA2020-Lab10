# Lab 10 : Rédiger et valider une revue systématique selon PRISMA 2020

**Manuscrit (anglais) :** *Machine learning and remote sensing for disease and stress detection in olive (Olea europaea L.): a systematic review of platforms, targets, algorithms and validation practice*
**Corpus :** 22 études (23 rapports) incluses après évaluation du texte intégral ; Scopus et Web of Science Core Collection, recherche du 15 novembre 2026, période 2013–2026.

Le manuscrit est rédigé en anglais au format de la classe Elsevier `elsarticle`, prêt à compiler sur Overleaf. Ses chiffres clés sont recalculés depuis les fichiers supplémentaires S1–S5 par `scripts/validate_manuscript_coherence.py`.

---

## 1. Prérequis

* Python ≥ 3.10 avec `pandas`, `numpy`, `scipy` (`pip install pandas numpy scipy`).
* Pour recompiler le manuscrit : `pdflatex` et `bibtex` (TeX Live), ou Overleaf. Pour la copie Markdown : `pandoc`.

## 2. Architecture du dépôt

```text
PRISMA2020-Lab10-main/
├── README.md
├── manuscript/
│   ├── systematic_review_prisma2020.tex      # Manuscrit de référence (elsarticle, anglais)
│   ├── refs_included.bib                     # Bibliographie (études incluses et références méthodologiques)
│   ├── systematic_review_prisma2020.pdf      # Version compilée (classe d'aperçu, voir § 4)
│   └── systematic_review_prisma2020.md       # Copie Markdown lisible sur GitHub (générée depuis le .tex)
├── figures/                                  # Figures du manuscrit, en PDF (LaTeX) et PNG (Markdown)
│   ├── Fig1_PRISMA_flow                      # Diagramme de flux PRISMA 2020 (Fig. 2 du PDF)
│   ├── Fig2_years_countries                  # Études par année et plateforme ; pays (Fig. 3)
│   ├── Fig3_platform_target                  # Plateforme × cible, résidus ajustés (Fig. 4)
│   ├── Fig4_performance_vs_validation        # Performance rapportée par niveau de validation (Fig. 5)
│   ├── Fig6_validation_deployment            # Niveaux V0–V5 et DRL1–5 (Fig. 6)
│   └── Fig5_quality_heatmap                  # Heatmap Q1–Q10 (Fig. 7)
├── supplementary/
│   ├── S1_screening_ledger.csv               # 143 notices : décision assistée, code, motif, re-sélection à l'aveugle
│   ├── S2_fulltext_eligibility.csv           # 53 rapports recherchés : obtention, décision, motif d'exclusion
│   ├── S3_fulltext_extraction_22_studies.csv # Extraction du texte intégral
│   ├── S4_quality_assessment_Q1-Q10.csv      # Scores Q1–Q10 (/20)
│   ├── S5_studies_master_v2.csv              # Données codées (plateforme, cible, V, DRL, scénarios, performance)
│   ├── lab8_consolidated_extraction_qa.csv   # S3 + S4 fusionnés (Lab 8)
│   ├── tableau_comparatif.csv, statistiques_performances.csv, limitations_frequentes.csv,
│   │   potential_gaps.csv, synthese_lab9.json # Sorties du Lab 9
│   ├── checklist_prisma2020_27items.md       # Checklist PRISMA 2020 (27 items et sous-items)
│   ├── verification_finale_lab10.md          # Tableau de validation, questions et défis 1–2
│   └── validation_coherence_lab10.json       # Rapport d'audit automatique
├── scripts/
│   ├── validate_manuscript_coherence.py      # Audit texte ↔ données ↔ figures (44 vérifications)
│   ├── build_manuscript.sh                   # Compile le .tex en PDF (pdflatex + bibtex)
│   ├── tex_to_markdown.py                    # Régénère la copie Markdown depuis le .tex
│   └── latex_preview/                        # Classe d'aperçu utilisée seulement si elsarticle n'est pas installé
└── tests/
    └── test_lab10.py                         # 7 tests : livrables, S1–S5, figures, citations, audit, checklist
```

## 3. Exécution

```bash
python3 scripts/validate_manuscript_coherence.py   # -> VALIDATED : 44/44
python3 -m unittest discover -s tests -v           # -> 7 tests OK
bash scripts/build_manuscript.sh                   # optionnel : recompile le PDF
python3 scripts/tex_to_markdown.py                 # optionnel : régénère la copie Markdown
```

## 4. Compilation du manuscrit

* **Overleaf (recommandé pour la soumission) :** importer `manuscript/` et `figures/` dans un même projet, garder l'arborescence (le `.tex` lit les figures via `\graphicspath{{../}}`, ou déplacer `figures/` à côté du `.tex` et supprimer cette ligne). La classe `elsarticle` y est disponible.
* **En local :** `scripts/build_manuscript.sh` utilise `elsarticle` si elle est installée ; sinon, il bascule sur une classe d'aperçu minimale (`scripts/latex_preview/`). Cette classe reproduit la zone de texte du gabarit Elsevier « preprint, 12pt » (police 12 pt, texte de 393 × 576 pt), d'où le même nombre de pages (64). Le contenu est identique ; seuls l'en-tête de première page et l'ordre de numérotation de quelques références (style `plainnat` au lieu de `elsarticle-num-names`) diffèrent. Le PDF fourni a été produit ainsi ; pour la soumission, compiler sur Overleaf avec la vraie classe.

## 5. Chiffres clés

* **Flux PRISMA :** 215 notices (Scopus 118, WoS 97) → 72 doublons → 143 examinées → 90 exclues → 53 recherchées → 15 non obtenues → 38 évaluées → 15 exclues → 23 rapports / 22 études (19 articles, 3 communications). Re-sélection à l'aveugle : 124/143 concordantes, κ = 0,70.
* **Corpus :** satellite 10, UAV 7, avion 5 ; multispectral 11, multimodal 6, RGB 3, hyperspectral 2 ; pathogènes vasculaires 11, stress hydrique 7, foliaire 2, mixte 2 ; ML classique 18, deep learning 4.
* **Preuves :** V0 1, V1 2, V2 8, V3 8, V4 3, V5 0 ; DRL2 11, DRL3 8, DRL4 3 ; QA médiane 10,5/20 (IQR 9–14) ; précision et validation : ρ = −0,70 ; plateforme × cible : χ² = 17,7, p = 0,002, V = 0,63.
* **Corrections par rapport à la version précédente de la revue :** titre « systematic mapping » → « systematic review » (item PRISMA 1) ; V de Cramér du scénario A = 0,63 (au lieu de 0,64) et V corrigé du scénario B = 0,51 (au lieu de 0,52), recalculés depuis S5.
