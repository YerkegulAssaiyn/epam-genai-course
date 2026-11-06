# Introduction module (intro)

This folder contains the deliverables for the EPAM “Generative AI for Software Development” Introduction module: a short research report on practical GenAI use cases and a companion vocabulary explaining key terms used in the report. It also includes artifacts generated from analyzing the terms (a small script, a JSON stats file, and a visualization).

## Files

- `research.md` — Research report describing 3 FinTech and 2 EdTech GenAI use cases, with cross-cutting observations.
- `vocabulary.md` – A concise glossary of GenAI terms used in the research report, explained in the author’s own words with examples.
- `build_graph.py` — Script that analyzes the terms and relationships and generates stats/visualizations for the intro materials.
- `terms_stats.json` – Machine-readable summary statistics produced from term analysis.
- `terms_graph.png` — Visualization of the terms/relationships produced by the analysis script.

## Vocabulary coverage check (vocabulary.md → research.md)

Result: all terms from `vocabulary.md` are present in `research.md`; unused terms: none.
