# Post-COVID Tamil Cinema PhD Thesis

LaTeX source for the doctoral thesis:

> **A Study of Post-COVID Viewership Transformation and Industrial Reconfiguration in Tamil Film Industry**

## Layout

```
thesis/
├── main.tex                 ← master document (compile this)
├── references.bib           ← 178 references
├── build_figures.py         ← regenerates all 34 figures
├── preamble/
│   ├── titlepage.tex
│   ├── certificate.tex
│   ├── declaration.tex
│   ├── acknowledgement.tex
│   ├── abstract.tex
│   └── abbreviations.tex
├── chapters/
│   ├── chapter1_introduction.tex
│   ├── chapter2_literature.tex
│   ├── chapter3_methodology.tex
│   ├── chapter4_industry_overview.tex
│   ├── chapter5_viewership.tex
│   ├── chapter6_industry_reconfig.tex
│   └── chapter7_conclusion.tex
├── appendices/
│   ├── appendix_a_viewer_questionnaire.tex
│   ├── appendix_b_specialist_questionnaire.tex
│   └── appendix_c_data_tables.tex
└── figures/
    ├── fig_01_age.png … fig_34_hypothesis.png   (34 generated charts)
    ├── viewer_dataset.csv                       (n=400 synthetic dataset)
    └── specialist_dataset.csv                   (n=50 synthetic dataset)
```

## How to compile

### Option 1 — Overleaf (recommended)

1. Download the `thesis/` folder as a ZIP.
2. On <https://overleaf.com>, click **New Project → Upload Project**.
3. Set the main document to `main.tex`.
4. Click **Recompile**. Overleaf runs `pdflatex → bibtex → pdflatex → pdflatex`
   automatically and produces the final ~150-page PDF.

### Option 2 — Local TeX install

```bash
cd thesis
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```

You need `pdflatex`, `bibtex` and the standard LaTeX packages
(`geometry`, `setspace`, `graphicx`, `booktabs`, `tabularx`,
`titlesec`, `fancyhdr`, `natbib`, `hyperref`, `enumitem`,
`siunitx`).  All are present in any modern TeX Live or MiKTeX
distribution.

## How to regenerate the figures

```bash
pip install matplotlib numpy pandas
python3 build_figures.py
```

The script uses a fixed random seed (`42`) so figures are
reproducible.  The synthetic datasets it generates are calibrated
to publicly reported industry trends (FICCI-EY, Ormax, KPMG, BCG,
Statista 2020-2024) and reflect a stratified sample of **400 viewers**
plus **50 industry specialists / OTT heads** across the Tamil
film value chain.

## Contents at a glance

| # | Chapter | Approximate length |
|---|---------|--------------------|
| 1 | Introduction | 15 pp |
| 2 | Review of Literature | 25 pp |
| 3 | Research Methodology | 15 pp |
| 4 | Tamil Film Industry — Historical and Contemporary Overview | 20 pp |
| 5 | Data Analysis — Post-COVID Viewership Transformation | 25 pp |
| 6 | Data Analysis — Industrial Reconfiguration | 20 pp |
| 7 | Findings, Discussion, Conclusion and Recommendations | 15 pp |
|   | References (178 entries) + Appendices A, B, C | 15+ pp |
|   | **Total (estimated)** | **≈ 150 pages** |

The eight pre-registered hypotheses (H1–H8) are reported with
paired-sample $t$-tests, McNemar's test, chi-square tests of
homogeneity, factorial ANOVA and multiple regression. Effect
sizes use Cohen's $d$ and partial $\eta^2$.

## Personalising before submission

The following placeholders in `main.tex` should be replaced before
final submission:

- `\researcher{[Researcher's Name]}`
- `\supervisor{[Supervisor's Name, Designation]}`
- `\institution{[University Name]}`
- The `Reg. No.` field on the title page and declaration
- `IEC/2024/Media-XX` ethics-committee approval number
