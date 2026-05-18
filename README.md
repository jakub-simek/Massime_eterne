# Massime eterne

Digital edition of *Massime eterne* by Saint Alphonsus Maria de Liguori, with translations and meditation-oriented companion texts.

## Project Rule

All project documentation, README files, and code comments must be written in English. Edition texts, source transcriptions, and translation content may remain in their source or target languages.

## Aim

This repository builds a text-aware but practically usable edition:

- an Italian base text from the freely accessible IntraText version;
- documented connection to the printed source named by IntraText;
- a German working translation and meditation layer, clearly separated from paraphrase and original meditation;
- TEI/XML as the edition-ready base format.

## Structure

- [docs/editorial-guidelines.md](docs/editorial-guidelines.md): editorial principles and working rules.
- [docs/intratext-to-tei-workflow.md](docs/intratext-to-tei-workflow.md): local workflow based on the `Glorie_di_Maria` project.
- [planning/meditations-guidelines.md](planning/meditations-guidelines.md): Massime-specific rules for paragraph-based Latin meditations.
- [sources/source-plan.md](sources/source-plan.md): source situation and prioritization.
- [data/bibliography.yml](data/bibliography.yml): growing bibliography scaffold.
- [edition/it/tei/](edition/it/tei/): Italian TEI base text.
- [edition/de/](edition/de/): German working translation.
- [meditations/](meditations/): meditation texts keyed to individual sections.

## Base Text

The initial Italian base text is the IntraText version:

`https://www.intratext.com/ixt/itasa0000/_IDX084.HTM`

IntraText names this printed source: S. Alfonso Maria de Liguori, *OPERE ASCETICHE*, Vol. IX, pp. 381-395, Edizioni di Storia e Letteratura, Roma 1965.

## First Steps

```sh
python3 scripts/download_intratext.py --fetcher curl --delay 0.5
python3 scripts/convert_intratext_to_tei.py
python3 -m xml.etree.ElementTree edition/it/tei/massime-eterne.xml
```

The workflow was adapted from `/Users/jakubsimek/GitLab/Glorie_di_Maria` and adjusted for the collection-level IntraText ID `ITASA0000`.
