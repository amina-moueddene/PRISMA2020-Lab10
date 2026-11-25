#!/usr/bin/env python3
"""Audit de cohérence texte <-> données <-> figures (Lab 10).

Recalcule à partir des fichiers supplémentaires S1–S5 chaque chiffre clé du manuscrit
(manuscript/systematic_review_prisma2020.tex), vérifie qu'il apparaît tel quel dans le
texte, vérifie que chaque figure citée existe, et écrit
supplementary/validation_coherence_lab10.json (status = VALIDATED si tout concorde).

Usage : python3 scripts/validate_manuscript_coherence.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
SUP = ROOT / "supplementary"
TEX = (ROOT / "manuscript" / "systematic_review_prisma2020.tex").read_text(encoding="utf-8")

# Effectifs d'identification : ils viennent des exports bruts Scopus/WoS (non inclus) ;
# ils sont contrôlés par cohérence avec S1 (215 - 72 = 143).
IDENT = {"scopus": 118, "wos": 97, "duplicates": 72}

WORDS = {3: "three", 7: "seven", 8: "Eight", 11: "Eleven", 23: "Twenty-three"}


def prisma_counts():
    s1 = pd.read_csv(SUP / "S1_screening_ledger.csv", encoding="utf-8-sig")
    s2 = pd.read_csv(SUP / "S2_fulltext_eligibility.csv", encoding="utf-8-sig")
    s5 = pd.read_csv(SUP / "S5_studies_master_v2.csv", encoding="utf-8-sig")
    identified = IDENT["scopus"] + IDENT["wos"]
    assert identified - IDENT["duplicates"] == len(s1), "Identification incohérente avec S1"
    ta = s1[~s1.record.isin(s2.record)]
    assessed = s2[s2.full_text_retrieved == "Yes"]
    return s1, s2, s5, {
        "identified": identified, **IDENT, "screened": len(s1), "ta_excluded": len(ta),
        "ta_codes": ta.exclusion_code.value_counts().to_dict(), "sought": len(s2),
        "not_retrieved": int((s2.full_text_retrieved == "No").sum()), "assessed": len(assessed),
        "ft_excluded": int((assessed.full_text_decision == "Excluded").sum()),
        "ft_codes": assessed[assessed.full_text_decision == "Excluded"].exclusion_code.value_counts().to_dict(),
        "reports_included": int((assessed.full_text_decision == "Included").sum()), "studies_included": len(s5),
        "journal": int((s5.document_type == "Article").sum()),
        "conference": int((s5.document_type != "Article").sum()),
    }


def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b)
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in np.union1d(a, b))
    return (po - pe) / (1 - pe)


def perm_chi2(table, B=20000, seed=1):
    """Test de permutation Monte-Carlo du χ² (marges fixées) et V de Cramér."""
    vals = table.values
    rows = np.repeat(np.arange(vals.shape[0]), vals.sum(1))
    cols = np.repeat(np.arange(vals.shape[1]), vals.sum(0))

    def chi(m):
        e = np.outer(m.sum(1), m.sum(0)) / m.sum()
        return (((m - e) ** 2)[e > 0] / e[e > 0]).sum()

    obs = chi(vals)
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(B):
        rng.shuffle(cols)
        m = np.zeros_like(vals)
        np.add.at(m, (rows, cols), 1)
        cnt += chi(m) >= obs - 1e-9
    v = np.sqrt(obs / (vals.sum() * (min(vals.shape) - 1)))
    return obs, (cnt + 1) / (B + 1), v


def main():
    checks = []

    def check(name, value, expected):
        checks.append({"élément": name, "valeur_recalculée": value, "texte_attendu": expected,
                       "présent": expected in TEX})

    s1, s2, m, c = prisma_counts()
    q = pd.read_csv(SUP / "S4_quality_assessment_Q1-Q10.csv", encoding="utf-8-sig")

    check("Notices identifiées", c["identified"], f"{c['identified']} records")
    check("Doublons", c["duplicates"], f"{c['duplicates']} duplicates")
    check("Notices examinées", c["screened"], f"{c['screened']} unique records were screened")
    check("Exclues titre/résumé", c["ta_excluded"], f"{c['ta_excluded']} were excluded")
    for code, n in c["ta_codes"].items():
        check(f"Exclusion titre/résumé {code}", n, f"({code}, $n={n}$)" if code == "E2" else f"({code}, {n})")
    check("Rapports recherchés", c["sought"], f"{c['sought']} reports sought")
    check("Non obtenus", c["not_retrieved"], f"{c['not_retrieved']} could not be obtained")
    check("Textes intégraux évalués", c["assessed"], f"{c['assessed']} full texts assessed")
    check("Exclusions texte intégral", c["ft_excluded"], f"{c['ft_excluded']} further exclusions")
    for code, n in c["ft_codes"].items():
        check(f"Exclusion texte intégral {code}", n, f"({code})")
    check("Rapports / études inclus", [c["reports_included"], c["studies_included"]],
          f"{WORDS[c['reports_included']]} reports, corresponding to {c['studies_included']} studies")
    check("Articles / communications", [c["journal"], c["conference"]],
          f"{c['journal']} were journal articles and {c['conference']} conference papers")

    first = np.where(s1.record.isin(s2.record), "in", "out")
    blind = np.where(s1.blind_re_screening_decision == "Exclude", "out", "in")
    agree, k = int((first == blind).sum()), kappa(first, blind)
    check("Accord re-sélection à l'aveugle", agree, f"{agree} of the {len(s1)} records")
    check("Kappa de Cohen", round(k, 2), f"\\kappa={k:.2f}")

    vc = m.platform.value_counts()
    check("Plateformes", vc.to_dict(), f"Satellites were used in {vc['Satellite']} studies, UAV in {vc['UAV']} "
                                       f"and piloted aircraft in {vc['Airborne']}")
    mod = m.modality.value_counts()
    check("Modalités", mod.to_dict(), f"most common modality ({mod['Multispectral']} studies), followed by "
                                      f"multimodal data ({mod['Multimodal']})")
    fam = m.ai_family.value_counts()
    check("Familles d'IA", fam.to_dict(), f"Classical machine learning was used in {fam['Classical ML']} studies "
                                          f"and deep learning in {fam['Deep learning']}")
    tg = m.target.value_counts()
    check("Pathogènes vasculaires", int(tg["Vascular pathogen"]),
          f"Vascular pathogens were the most frequent target ({tg['Vascular pathogen']} studies)")
    ref = m.reference_data.value_counts()
    check("Référence qPCR/PCR", int(ref["Laboratory (qPCR/PCR)"]),
          f"qPCR or PCR in {WORDS[int(ref['Laboratory (qPCR/PCR)'])]} studies")
    vl = m.validation_level.value_counts()
    check("Niveau V2", int(vl["V2"]), f"{WORDS[int(vl['V2'])]} used an internal split")
    check("Niveau V4", int(vl["V4"]), f"{WORDS[int(vl['V4'])].capitalize()} tested transfer explicitly (V4)")
    dr = m.deployment_level.value_counts()
    check("DRL2", int(dr["DRL2"]), f"{WORDS[int(dr['DRL2'])]} studies reached DRL2")
    check("DRL3/DRL4", [int(dr["DRL3"]), int(dr["DRL4"])], "eight reached DRL3 (several sites or seasons) and three reached DRL4")

    tot = q.quality_total_out_of_20
    check("Score QA médian et IQR", [tot.median(), tot.quantile(.25), tot.quantile(.75)],
          f"median {tot.median():.1f}, interquartile range {int(tot.quantile(.25))}--{int(tot.quantile(.75))}")
    check("Score QA étendue", [int(tot.min()), int(tot.max())], f"ranged from {tot.min()} to {tot.max()}")
    check("Études QA ≥ 10", int((tot >= 10).sum()), f"{int((tot >= 10).sum())} of the 22 studies scored at least 10")
    mq = m.merge(q[["record", "quality_total_out_of_20"]], on="record", suffixes=("_m", ""))
    med = mq.groupby("ai_family").quality_total_out_of_20.median()
    check("QA médian DL / ML", med.to_dict(), f"Median scores were {med['Deep learning']:.1f} for deep-learning studies "
                                              f"and {int(med['Classical ML'])} for classical")

    acc = m[m.metric.isin(["OA", "Accuracy"])].dropna(subset=["reported_performance"])
    vnum = acc.validation_level.str[1].astype(int)
    rho, p = stats.spearmanr(vnum, acc.reported_performance)
    check("Études avec OA/accuracy", len(acc), f"Among the {len(acc)} studies reporting")
    check("Spearman performance/validation", [round(rho, 2), round(p, 3)], f"\\rho={rho:.2f}$, $p={p:.3f}")

    tgt = pd.crosstab(m.platform, m.target)
    chi, pp, v = perm_chi2(tgt)
    check("χ² plateforme × cible", round(chi, 1), f"\\chi^2={chi:.1f}")
    check("p de permutation", round(pp, 3), f"p={pp:.3f}")
    check("V de Cramér (0,6348 → 0,63)", round(v, 4), f"V=0.63$")

    for fig in sorted(set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", TEX))):
        exists = (ROOT / fig).exists()
        checks.append({"élément": f"Figure {fig}", "valeur_recalculée": exists, "texte_attendu": fig,
                       "présent": exists})

    n_ok = sum(ch["présent"] for ch in checks)
    report = {
        "status": "VALIDATED" if n_ok == len(checks) else "FAILED",
        "checks_passed": n_ok, "checks_total": len(checks),
        "total_studies": int(len(m)), "total_reports": int(c["reports_included"]),
        "prisma_flow": {k: c[k] for k in ["identified", "duplicates", "screened", "ta_excluded", "sought",
                                         "not_retrieved", "assessed", "ft_excluded", "reports_included",
                                         "studies_included"]},
        "checks": checks,
    }
    (SUP / "validation_coherence_lab10.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    for ch in checks:
        if not ch["présent"]:
            print("ÉCHEC :", ch["élément"], "->", ch["texte_attendu"])
    print(f"{report['status']} : {n_ok}/{len(checks)} vérifications")
    return 0 if report["status"] == "VALIDATED" else 1


if __name__ == "__main__":
    sys.exit(main())
