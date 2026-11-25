#!/usr/bin/env bash
# Compile manuscript/systematic_review_prisma2020.tex -> .pdf (pdflatex + bibtex).
# The manuscript uses the Elsevier class "elsarticle" (available on Overleaf and in full TeX Live).
# If it is not installed locally, a minimal preview class from scripts/latex_preview/ is used instead:
# the content is identical, only the page layout differs from the journal template.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/manuscript"
if ! kpsewhich elsarticle.cls >/dev/null 2>&1; then
  echo "elsarticle.cls introuvable : utilisation de la classe d'aperçu (scripts/latex_preview/)."
  export TEXINPUTS=".:$ROOT/scripts/latex_preview//:"
  export BSTINPUTS=".:$ROOT/scripts/latex_preview//:"
fi
pdflatex -interaction=nonstopmode systematic_review_prisma2020.tex >/dev/null || true
bibtex systematic_review_prisma2020 >/dev/null
pdflatex -interaction=nonstopmode systematic_review_prisma2020.tex >/dev/null || true
pdflatex -interaction=nonstopmode systematic_review_prisma2020.tex >/dev/null || true
if grep -q "^!" systematic_review_prisma2020.log; then grep -A2 "^!" systematic_review_prisma2020.log; exit 1; fi
rm -f systematic_review_prisma2020.{aux,log,out,blg,bbl,spl,toc}
echo "OK : manuscript/systematic_review_prisma2020.pdf"
