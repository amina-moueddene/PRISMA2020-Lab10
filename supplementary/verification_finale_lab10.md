# Vérification finale et réponses aux défis — Lab 10 (PRISMA 2020)

Le manuscrit est la revue systématique elle-même, rédigée en anglais pour une revue Elsevier (`manuscript/systematic_review_prisma2020.tex`). Les numéros de section, de tableau et de figure renvoient au PDF compilé.

## 1. Tableau de validation de cohérence (Étape 16)

| Élément | Présent ? | Localisation exacte | Correction nécessaire |
| :--- | :---: | :--- | :---: |
| **Titre explicite** | Oui | Titre du manuscrit (« …: a systematic review of platforms, targets, algorithms and validation practice ») | Non (corrigé : « systematic mapping » remplacé par « systematic review ») |
| **Résumé structuré** | Oui | Abstract : objectif, sources, sélection, résultats, certitude | Non |
| **Introduction et RQ1–RQ5** | Oui | Section 1 ; Table 2 ; cadre d'analyse Fig. 1 | Non |
| **Méthodes** | Oui | Sections 2.1–2.12 ; Tables 3 (équations), 4 (critères E1–E8), 5 (échelles V et DRL), 16 (Q1–Q10) | Non |
| **Diagramme de flux PRISMA 2020** | Oui | Section 3.1 ; Fig. 2 (`figures/Fig1_PRISMA_flow.pdf`) | Non |
| **Tableau des 22 études** | Oui | Table 7 (caractéristiques) ; Table 8 (performances) | Non |
| **Résultats organisés par RQ1–RQ5** | Oui | Sections 3.2–3.10 (titres « RQ1 » à « RQ5 ») | Non |
| **Figures** | Oui | Fig. 1–7 ; fichiers PDF et PNG dans `figures/` | Non |
| **Qualité Q1–Q10** | Oui | Section 3.9 ; Fig. 7 ; S4 | Non |
| **Sensibilité et certitude des preuves** | Oui | Tables 10 et 11 | Non |
| **Discussion, lacunes, benchmark, limites** | Oui | Sections 4–7 ; Tables 12–15 | Non |
| **Conclusion et références** | Oui | Section 8 ; bibliographie (`refs_included.bib`) | Non |
| **Checklist PRISMA 2020 (27 items)** | Oui | `supplementary/checklist_prisma2020_27items.md` et Appendix B | Non |

## 2. Réponses aux questions de vérification finale

1. **Le titre est-il explicite et informatif ?**
   Oui. *Machine learning and remote sensing for disease and stress detection in olive (Olea europaea L.): a systematic review of platforms, targets, algorithms and validation practice* nomme la culture, les cibles, les technologies et l'objet de l'analyse, et identifie l'article comme une revue systématique (item PRISMA 1). La version précédente disait « systematic mapping » ; elle a été corrigée.
2. **Les RQ sont-elles clairement définies et répondues ?**
   Oui. Les cinq RQ du protocole (Table 2) sont reprises dans les titres des sous-sections de résultats : RQ1 en 3.2 et 3.6, RQ2 en 3.3, RQ3 en 3.4 et 3.8, RQ4 en 3.5, 3.7 et 3.9, RQ5 en 3.10 et Sections 5–6.
3. **Le protocole est-il décrit avec suffisamment de détails ?**
   Oui. Deux bases (Scopus, Web of Science Core Collection) interrogées le 15 novembre 2026 avec les équations exactes (Table 3) ; déduplication par DOI puis par titre (215 → 143) ; huit critères avec codes E1–E8 (Table 4) ; sélection en deux étapes avec re-sélection à l'aveugle (κ = 0,70) ; formulaire d'extraction en six domaines ; échelles V0–V5 et DRL1–5 ; grille Q1–Q10 ; règle de certitude inspirée de GRADE. Les écarts (évaluateur unique, protocole non enregistré) sont déclarés en Section 7.
4. **Le diagramme PRISMA est-il cohérent avec les données ?**
   Oui, vérifié automatiquement depuis S1 et S2 : 215 notices − 72 doublons = 143 examinées ; − 90 exclues (E2 36, E3 17, E7 14, E4 12, E6 11) = 53 recherchées ; − 15 non obtenues = 38 évaluées ; − 15 exclues (E3 5, E4 5, E5 5) = 23 rapports, soit 22 études (19 articles, 3 communications).
5. **La checklist PRISMA est-elle complétée et jointe ?**
   Oui, avec ses sous-items (10a/b, 13a–f, 16a/b, 20a–d, 23a–d, 24a–c). Six items sont « Partly » (8, 9, 21, 24a, 24b, 27) : les écarts sont déclarés, pas masqués.

## 3. Défis 1 et 2

* **Défi 1 (reproductibilité) :** un chercheur tiers dispose des équations exactes (Table 3), des cinq fichiers de la revue (S1 registre de sélection, S2 évaluation du texte intégral, S3 extraction, S4 qualité, S5 données codées), du pipeline d'analyse du Lab 9, des scripts de ce dépôt et des sources LaTeX et BibTeX du manuscrit. Seuls les exports bruts des deux bases (215 notices) ne sont pas inclus ; leurs effectifs sont contrôlés par cohérence (215 − 72 = 143 lignes de S1).
* **Défi 2 (vérification croisée texte ↔ données ↔ figures) :** `scripts/validate_manuscript_coherence.py` recalcule depuis S1–S5 les chiffres clés (flux PRISMA et codes d'exclusion, κ, plateformes, modalités, cibles, familles d'IA, niveaux V et DRL, scores qualité, ρ de Spearman, χ² de permutation, V de Cramér) et vérifie qu'ils figurent tels quels dans le `.tex`, ainsi que l'existence de chaque figure incluse. Résultat : `VALIDATED`, 44/44 (`supplementary/validation_coherence_lab10.json`).
  * L'audit a révélé deux erreurs d'arrondi dans la version précédente de la revue, corrigées dans le manuscrit : V de Cramér du scénario A = 0,6348, donc **0.63** (et non 0.64 : résumé, Section 3.3, légende de la Fig. 4, Table 10) ; V corrigé du biais du scénario B = 0,5146, donc **0.51** (et non 0.52, Table 10).
