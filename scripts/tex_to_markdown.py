#!/usr/bin/env python3
"""Convert manuscript/systematic_review_prisma2020.tex into a readable Markdown copy
(manuscript/systematic_review_prisma2020.md) for viewing on GitHub.

The LaTeX file is the reference version. This script:
  * takes cross-reference numbers (tables, figures, sections) from the .aux file of a
    LaTeX compilation, so "Table 4" in the Markdown matches the PDF;
  * rewrites the Elsevier front matter (title, abstract, keywords) as Markdown;
  * points figures to the PNG copies in figures/;
  * resolves citations with pandoc --citeproc and refs_included.bib.

Usage : python3 scripts/tex_to_markdown.py   (needs pandoc, pdflatex and bibtex)
"""
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"
TEX = MAN / "systematic_review_prisma2020.tex"


def compile_aux(workdir: Path) -> str:
    env = dict(os.environ)
    try:
        subprocess.run(["kpsewhich", "elsarticle.cls"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        prev = str(ROOT / "scripts" / "latex_preview") + "//:"
        env["TEXINPUTS"] = f".:{prev}{ROOT}//:"
        env["BSTINPUTS"] = f".:{prev}"
    for cmd in (["pdflatex", "-interaction=nonstopmode", TEX.name], ["bibtex", TEX.stem],
                ["pdflatex", "-interaction=nonstopmode", TEX.name]):
        subprocess.run(cmd, cwd=workdir, env=env, capture_output=True)
    return (workdir / f"{TEX.stem}.aux").read_text(encoding="utf-8", errors="ignore")


def labels(aux: str) -> dict:
    out = {}
    for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", aux):
        out[m.group(1)] = m.group(2)
    return out


def preprocess(tex: str, lab: dict) -> str:
    tex = re.sub(r"\\ref\{([^}]+)\}", lambda m: lab.get(m.group(1), m.group(1)), tex)
    tex = tex.replace("~", " ")
    title = re.search(r"\\title\{(.*?)\}\n", tex, re.S).group(1)
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1).strip()
    keywords = re.search(r"\\begin\{keyword\}(.*?)\\end\{keyword\}", tex, re.S).group(1).strip()
    keywords = re.sub(r"\s*\\sep\s*", "; ", keywords)
    front = (f"\\section*{{{title}}}\n\n\\textbf{{Abstract.}} {abstract}\n\n"
             f"\\textbf{{Keywords:}} {keywords}\n\n")
    tex = re.sub(r"\\begin\{frontmatter\}.*?\\end\{frontmatter\}", lambda m: front, tex, flags=re.S)
    tex = re.sub(r"figures/(Fig\d_[A-Za-z_]+)\.pdf", r"../figures/\1.png", tex)
    # Table constructs pandoc does not read: custom column type, landscape, resizebox, longtable heads.
    tex = re.sub(r"L\{([^}]*)\}", r"p{\1}", tex)
    tex = re.sub(r"\\(begin|end)\{landscape\}", "", tex)
    tex = re.sub(r"\\resizebox\{[^}]*\}\{!\}\{%?\s*(\\begin\{tabular\}.*?\\end\{tabular\})\}", r"\1", tex, flags=re.S)
    tex = re.sub(r"\\endfirsthead.*?\\endhead", "", tex, flags=re.S)
    tex = re.sub(r"\\bottomrule\\endfoot", "", tex)
    tex = re.sub(r"\\(setlength\\tabcolsep\{[^}]*\}|renewcommand\{\\arraystretch\}\{[^}]*\}|setlength\\tabcolsep[0-9.]+pt)", "", tex)
    tex = re.sub(r"\\makecell\{([^}]*)\}", lambda m: m.group(1).replace("\\\\", " "), tex)
    for code, sym in (("108", "●"), ("119", "◐"), ("109", "○")):
        tex = tex.replace("\\ding{%s}" % code, sym)
    tex = re.sub(r"\\\[\d+pt\]", r"\\\\", tex)
    tex = re.sub(r"\\multicolumn\{(\d+)\}\{[^{}]*(?:\{[^}]*\}[^{}]*)*\}", r"\\multicolumn{\1}{l}", tex)
    tex = re.sub(r"\\citet\{([^},]+,[^}]+)\}", r"\\citep{\1}", tex)  # several keys: parenthetical list
    tex = tex.replace("\\bibliographystyle", "\\section*{References}\n\\bibliographystyle")
    # The analytical framework (TikZ) cannot be converted: point the reader to the PDF.
    tex = re.sub(r"\\resizebox\{\\linewidth\}\{!\}\{\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}\}",
                 lambda m: r"\emph{[Diagram drawn in TikZ: see the PDF version.]}", tex, flags=re.S)
    return tex


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for f in MAN.iterdir():
            if f.suffix in {".tex", ".bib"}:
                shutil.copy(f, tmp)
        lab = labels(compile_aux(tmp))
        src = tmp / "pre.tex"
        src.write_text(preprocess(TEX.read_text(encoding="utf-8"), lab), encoding="utf-8")
        out = MAN / "systematic_review_prisma2020.md"
        subprocess.run(["pandoc", str(src), "-f", "latex", "-t", "gfm", "--citeproc",
                        f"--bibliography={MAN / 'refs_included.bib'}", "--wrap=none", "-o", str(out)], check=True)
    md = out.read_text(encoding="utf-8")
    md = re.sub(r'<a href="#[^"]*" data-reference-type="ref" data-reference="[^"]*">\[?([^<\]]*)\]?</a>', r"\1", md)
    md = md.replace("<!-- -->", "")
    note = ("> Markdown copy generated from `systematic_review_prisma2020.tex` by `scripts/tex_to_markdown.py`. "
            "The LaTeX/PDF version is the reference (numbered citations, journal layout).\n\n")
    out.write_text(note + md, encoding="utf-8")
    print(f"OK : {out.relative_to(ROOT)} ({len(md.split())} words, {len(lab)} cross-references resolved)")


if __name__ == "__main__":
    main()
