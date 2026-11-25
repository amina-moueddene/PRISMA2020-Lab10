#!/usr/bin/env python3
"""Reproducible generation of high-resolution (300 DPI) PRISMA 2020 figures from S1-S5.

Generates Fig1_PRISMA_flow through Fig6_validation_deployment in both vector PDF
and 300 DPI raster PNG formats directly from the supplementary CSV datasets.

Usage:
    python3 scripts/generate_figures.py --output-dir figures
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = Path(__file__).resolve().parent.parent
SUP = ROOT / "supplementary"
SEED = 42


def save_dual(fig: plt.Figure, out_dir: Path, stem: str, dpi: int = 300) -> None:
    """Save figure in both vector PDF and 300 DPI PNG formats."""
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"{stem}.pdf", bbox_inches="tight", dpi=dpi)
    fig.savefig(out_dir / f"{stem}.png", bbox_inches="tight", dpi=dpi)
    plt.close(fig)


def plot_fig1_prisma(s1: pd.DataFrame, s2: pd.DataFrame, s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate PRISMA 2020 flow diagram from S1, S2, and S5."""
    identified = 215
    duplicates = 72
    screened = len(s1)
    ta_excl = len(s1[~s1.record.isin(s2.record)])
    sought = len(s2)
    not_retr = int((s2.full_text_retrieved == "No").sum())
    assessed = int((s2.full_text_retrieved == "Yes").sum())
    ft_excl = int((s2[s2.full_text_retrieved == "Yes"].full_text_decision == "Excluded").sum())
    reports_inc = int((s2[s2.full_text_retrieved == "Yes"].full_text_decision == "Included").sum())
    studies_inc = len(s5)

    fig, ax = plt.subplots(figsize=(8.5, 8.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    boxes = [
        (0.8, 8.3, 4.0, 1.2, f"Records identified from databases (n = {identified})\nScopus (n = 118)\nWeb of Science Core Collection (n = 97)", "#ffffff"),
        (5.5, 8.3, 4.0, 1.2, f"Records removed before screening:\nduplicates (n = {duplicates};\n70 by DOI, 2 by normalised title)", "#ffffff"),
        (0.8, 6.4, 4.0, 1.0, f"Records screened on title and abstract\n(n = {screened})", "#ffffff"),
        (5.5, 5.9, 4.0, 1.9, f"Records excluded (n = {ta_excl}):\nE2 (n = 36), E3 (n = 17), E7 (n = 14),\nE4 (n = 12), E6 (n = 11)", "#ffffff"),
        (0.8, 4.5, 4.0, 1.0, f"Reports sought for retrieval\n(n = {sought})", "#ffffff"),
        (5.5, 4.5, 4.0, 1.0, f"Reports not retrieved (n = {not_retr})\n(first-stage: include 11, uncertain 4)", "#ffffff"),
        (0.8, 2.6, 4.0, 1.0, f"Full-text reports assessed for eligibility\n(n = {assessed})", "#ffffff"),
        (5.5, 2.3, 4.0, 1.5, f"Reports excluded (n = {ft_excl}):\nE3 (n = 5), E4 (n = 5), E5 (n = 5)", "#ffffff"),
        (0.8, 0.4, 4.0, 1.3, f"Studies included in the review (n = {studies_inc})\nReports of included studies (n = {reports_inc})\n(19 journal articles, 3 conference papers)", "#d4e6f9"),
    ]
    for x, y, w, h, text, fc in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", linewidth=1.2, edgecolor="#333333", facecolor=fc)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5, fontweight="bold" if fc != "#ffffff" else "normal")

    arrows = [
        ((4.88, 8.9), (5.42, 8.9)),
        ((2.8, 8.22), (2.8, 7.48)),
        ((4.88, 6.9), (5.42, 6.9)),
        ((2.8, 6.32), (2.8, 5.58)),
        ((4.88, 5.0), (5.42, 5.0)),
        ((2.8, 4.42), (2.8, 3.68)),
        ((4.88, 3.1), (5.42, 3.1)),
        ((2.8, 2.52), (2.8, 1.78)),
    ]
    for p1, p2 in arrows:
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", lw=1.2, color="#333333"))

    save_dual(fig, out_dir, "Fig1_PRISMA_flow")


def plot_fig2_years_countries(s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate temporal and geographic distribution figure from S5."""
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
    years = list(range(2015, 2027))
    ct_year = pd.crosstab(s5["year"], s5["platform"]).reindex(years, fill_value=0)
    colors = {"UAV": "#2b7de9", "Airborne": "#eb6734", "Satellite": "#17a673"}
    bottom = np.zeros(len(years))
    for plat in ["UAV", "Airborne", "Satellite"]:
        vals = ct_year[plat].values if plat in ct_year else np.zeros(len(years))
        axes[0].bar(years, vals, bottom=bottom, label=plat, color=colors[plat], width=0.65)
        bottom += vals
    axes[0].set_title("a  Year of publication and platform", loc="left", fontweight="bold")
    axes[0].set_ylabel("Studies")
    axes[0].set_xticks(years)
    axes[0].set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    axes[0].legend(frameon=False, ncol=3)
    axes[0].spines[["top", "right"]].set_visible(False)

    ct_country = s5["country"].value_counts().sort_values(ascending=True)
    axes[1].barh(ct_country.index, ct_country.values, color="#4a90e2", height=0.6)
    for idx, v in enumerate(ct_country.values):
        axes[1].text(v + 0.15, idx, str(v), va="center", fontsize=9)
    axes[1].set_title("b  Country of the study area", loc="left", fontweight="bold")
    axes[1].set_xlim(0, ct_country.max() + 1)
    axes[1].spines[["top", "right", "bottom"]].set_visible(False)
    axes[1].xaxis.set_visible(False)

    fig.tight_layout()
    save_dual(fig, out_dir, "Fig2_years_countries")


def plot_fig3_platform_target(s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate platform x target contingency matrix with adjusted Pearson residuals."""
    platforms = ["UAV", "Airborne", "Satellite"]
    targets = ["Vascular pathogen", "Foliar disease", "Mixed biotic/abiotic stress", "Water/drought stress"]
    ct = pd.crosstab(s5["platform"], s5["target"]).reindex(index=platforms, columns=targets, fill_value=0)
    obs = ct.values.astype(float)
    n = obs.sum()
    r_sum = obs.sum(axis=1, keepdims=True)
    c_sum = obs.sum(axis=0, keepdims=True)
    exp = r_sum @ c_sum / n
    adj_res = (obs - exp) / np.sqrt(exp * (1 - r_sum / n) * (1 - c_sum / n))

    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    im = ax.imshow(adj_res, cmap="coolwarm_r", vmin=-3, vmax=3, aspect="auto")
    for i in range(len(platforms)):
        for j in range(len(targets)):
            val = int(obs[i, j])
            res = adj_res[i, j]
            star = "*" if abs(res) >= 1.96 else ""
            col = "white" if abs(res) > 1.8 else "black"
            ax.text(j, i - 0.12, f"{val}", ha="center", va="center", fontsize=13, fontweight="bold", color=col)
            ax.text(j, i + 0.22, f"{res:+.1f}{star}", ha="center", va="center", fontsize=9.5, color=col)
    ax.set_xticks(range(len(targets)))
    ax.set_xticklabels(["Vascular\npathogen", "Foliar\ndisease", "Mixed biotic/\nabiotic stress", "Water/drought\nstress"])
    ax.set_yticks(range(len(platforms)))
    ax.set_yticklabels([f"{p} (n = {int(r_sum[i, 0])})" for i, p in enumerate(platforms)])
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.03)
    cbar.set_label("Adjusted standardised residual")
    fig.tight_layout()
    save_dual(fig, out_dir, "Fig3_platform_target")


def plot_fig4_performance_vs_validation(s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate reported headline performance across validation levels V1-V4."""
    df = s5.dropna(subset=["reported_performance"]).copy()
    df["v_order"] = df["validation_level"].str[1].astype(int)
    df = df.sort_values(["v_order", "reported_performance"], ascending=[True, True])

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    target_colors = {
        "Vascular pathogen": "#2b7de9",
        "Foliar disease": "#eb6734",
        "Mixed biotic/abiotic stress": "#f5a623",
        "Water/drought stress": "#17a673",
    }
    y_pos = np.arange(len(df))
    for idx, (_, row) in enumerate(df.iterrows()):
        c = target_colors.get(row["target"], "#333333")
        ax.hlines(idx, 0, row["reported_performance"], color="#e0e0e0", lw=1)
        ax.scatter(row["reported_performance"], idx, color=c, s=55, zorder=3)
        ax.text(row["reported_performance"] + 0.012, idx, f"{row['reported_performance']:.2f}", va="center", fontsize=8.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{r.first_author} {r.year} ({r.validation_level})" for _, r in df.iterrows()], fontsize=8.5)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("Headline value as reported (internal validation unless marked)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_dual(fig, out_dir, "Fig4_performance_vs_validation")


def plot_fig5_quality_heatmap(s4: pd.DataFrame, s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate methodological quality heatmap Q1-Q10 (/20) from S4 and S5."""
    df = s4.merge(s5[["record", "platform"]], on="record").sort_values("quality_total_out_of_20", ascending=True)
    q_cols = [f"Q{i}" for i in range(1, 11)]
    mat = df[q_cols].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 7.2), gridspec_kw={"width_ratios": [4.2, 1.2]})
    cmap = matplotlib.colors.ListedColormap(["#efefef", "#7fb3eb", "#1a5fb4"])
    ax1.imshow(mat, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = int(mat[i, j])
            ax1.text(j, i, str(val), ha="center", va="center", fontsize=8.5, color="white" if val == 2 else "black")
    ax1.set_xticks(range(10))
    ax1.set_xticklabels(q_cols)
    ax1.set_yticks(range(len(df)))
    ax1.set_yticklabels([f"{r.first_author} {r.year} ({r.platform[0]})" for _, r in df.iterrows()], fontsize=8.5)

    plat_colors = {"UAV": "#2b7de9", "Airborne": "#eb6734", "Satellite": "#17a673"}
    bar_colors = [plat_colors[p] for p in df["platform"]]
    ax2.barh(range(len(df)), df["quality_total_out_of_20"], color=bar_colors, height=0.65)
    ax2.axvline(10, color="#666666", linestyle=":", lw=1)
    for i, tot in enumerate(df["quality_total_out_of_20"]):
        ax2.text(tot + 0.4, i, str(tot), va="center", fontsize=8.5)
    ax2.set_xlim(0, 21)
    ax2.set_title("Total /20", fontsize=9.5)
    ax2.set_yticks(range(len(df)))
    ax2.set_yticklabels([])
    ax2.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    save_dual(fig, out_dir, "Fig5_quality_heatmap")


def plot_fig6_validation_deployment(s5: pd.DataFrame, out_dir: Path) -> None:
    """Generate validation rigour (V0-V4) and deployment readiness (DRL1-DRL5) figure."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.4), gridspec_kw={"width_ratios": [2.2, 1.0]})
    v_levels = ["V0", "V1", "V2", "V3", "V4"]
    v_colors = ["#cde2f7", "#7fb3eb", "#4a90e2", "#1e65b8", "#0d3b75"]

    groups = [
        ("Classical ML", s5[s5.ai_family == "Classical ML"]),
        ("Deep learning", s5[s5.ai_family == "Deep learning"]),
        ("Water/drought stress", s5[s5.target == "Water/drought stress"]),
        ("Mixed biotic/abiotic stress", s5[s5.target == "Mixed biotic/abiotic stress"]),
        ("Foliar disease", s5[s5.target == "Foliar disease"]),
        ("Vascular pathogen", s5[s5.target == "Vascular pathogen"]),
    ]
    for y_idx, (label, sub) in enumerate(groups):
        left = 0
        for v, col in zip(v_levels, v_colors):
            cnt = int((sub.validation_level == v).sum())
            if cnt > 0:
                ax1.barh(y_idx, cnt, left=left, color=col, height=0.6, edgecolor="white")
                ax1.text(left + cnt / 2, y_idx, str(cnt), ha="center", va="center",
                         color="white" if v in ["V2", "V3", "V4"] else "black", fontsize=8.5)
                left += cnt
    ax1.set_yticks(range(len(groups)))
    ax1.set_yticklabels([f"{lbl} (n = {len(sub)})" for lbl, sub in groups], fontsize=8.5)
    ax1.set_xlabel("Studies")
    ax1.set_title("a  Validation-rigour level", loc="left", fontweight="bold")
    ax1.spines[["top", "right"]].set_visible(False)

    drls = ["DRL1", "DRL2", "DRL3", "DRL4", "DRL5"]
    drl_counts = [int((s5.deployment_level == d).sum()) for d in drls]
    ax2.bar(drls, drl_counts, color=["#cde2f7", "#7fb3eb", "#1e65b8", "#0d3b75", "#08254a"], width=0.55)
    for idx, cnt in enumerate(drl_counts):
        ax2.text(idx, cnt + 0.25, str(cnt), ha="center", fontsize=9)
    ax2.set_ylim(0, 12.5)
    ax2.set_title("b  Deployment-readiness level", loc="left", fontweight="bold")
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.yaxis.set_visible(False)

    fig.tight_layout()
    save_dual(fig, out_dir, "Fig6_validation_deployment")


def generate_all_figures(output_dir: Path) -> list[Path]:
    """Load S1-S5 datasets and generate all 6 PRISMA 2020 figures at 300 DPI."""
    np.random.seed(SEED)
    s1 = pd.read_csv(SUP / "S1_screening_ledger.csv", encoding="utf-8-sig")
    s2 = pd.read_csv(SUP / "S2_fulltext_eligibility.csv", encoding="utf-8-sig")
    s4 = pd.read_csv(SUP / "S4_quality_assessment_Q1-Q10.csv", encoding="utf-8-sig")
    s5 = pd.read_csv(SUP / "S5_studies_master_v2.csv", encoding="utf-8-sig")

    plot_fig1_prisma(s1, s2, s5, output_dir)
    plot_fig2_years_countries(s5, output_dir)
    plot_fig3_platform_target(s5, output_dir)
    plot_fig4_performance_vs_validation(s5, output_dir)
    plot_fig5_quality_heatmap(s4, s5, output_dir)
    plot_fig6_validation_deployment(s5, output_dir)

    return sorted(output_dir.glob("Fig*.*"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate high-resolution PRISMA 2020 figures (300 DPI).")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "figures", help="Output directory for PDF/PNG figures")
    args = parser.parse_args()
    files = generate_all_figures(args.output_dir)
    print(f"Generated {len(files)} figure files (300 DPI) in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
