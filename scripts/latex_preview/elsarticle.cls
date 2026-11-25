\NeedsTeXFormat{LaTeX2e}\ProvidesClass{elsarticle}[2026/01/01 v0 local preview shim]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}\ProcessOptions\relax
\LoadClass[12pt]{article}
\RequirePackage[letterpaper,textwidth=393pt,textheight=576pt,top=118pt,hcentering]{geometry}\RequirePackage[numbers,sort&compress]{natbib}
\newcommand{\journal}[1]{}\newcommand{\biboptions}[1]{}
\newcommand{\ead}[1]{}\newcommand{\cortext}[2][]{}\newcommand{\corref}[1]{}
\gdef\@allauthors{}\renewcommand{\author}[2][]{\g@addto@macro\@allauthors{#2\quad}}
\newcommand{\affiliation}[2][]{}
\newenvironment{frontmatter}{}{\vspace{1em}}
\renewenvironment{abstract}{\begin{center}{\LARGE\bfseries\@title\par}\vspace{1em}{\large\@allauthors\par}\end{center}\section*{Abstract}}{\par}
\newcommand{\sep}{\unskip; }
\newenvironment{keyword}{\par\vspace{.5em}\noindent\textbf{Keywords:} }{\par}
\renewcommand{\maketitle}{}
