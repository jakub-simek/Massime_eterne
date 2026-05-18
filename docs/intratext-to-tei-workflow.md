# IntraText To TEI: Workflow For Massime eterne

This repository uses the IntraText workflow from `/Users/jakubsimek/GitLab/Glorie_di_Maria` as its model.

## Source

- Work: *Massime eterne*, cioe meditazioni per ciascun giorno della settimana
- Author: S. Alfonso Maria de Liguori
- IntraText collection: `ITASA0000`
- Work index: `https://www.intratext.com/ixt/itasa0000/_IDX084.HTM`
- Printed source named by IntraText: S. Alfonso Maria de Liguori, *OPERE ASCETICHE*, Vol. IX, pp. 381-395, Edizioni di Storia e Letteratura, Roma 1965
- Electronic transcription named by IntraText: P. Salvatore Brugnano, CSSR
- ETML markup named by IntraText: EuloTech

## Download

The downloader is:

```text
scripts/download_intratext.py
```

It downloads the work index `_IDX084.HTM`, extracts linked text pages matching `_P*.HTM`, converts them to the hidden-concordance variants `__P*.HTM`, and writes:

```text
sources/intratext/raw_html/
sources/intratext/manifest.json
```

Run:

```sh
python3 scripts/download_intratext.py --fetcher curl --delay 0.5
```

## Conversion

The converter is:

```text
scripts/convert_intratext_to_tei.py
```

It first creates a conservative TEI version organized by IntraText page:

```text
edition/it/tei/massime-eterne.xml
```

The conversion preserves:

- paragraphs as `<p>`;
- italic and bold text as `<hi rend="italic">` and `<hi rend="bold">`;
- footnote references as `<ref type="note">`;
- footnotes in the back matter as `<note>`;
- printed pages as `<pb>`;
- IntraText pages as `<milestone unit="intratext-page">`.

## Validation

```sh
python3 -m json.tool sources/intratext/manifest.json >/dev/null
python3 -m xml.etree.ElementTree edition/it/tei/massime-eterne.xml
```

Useful checks:

```sh
rg '<ref type="note"' edition/it/tei/massime-eterne.xml
rg '<note xml:id=' edition/it/tei/massime-eterne.xml
rg '<pb ' edition/it/tei/massime-eterne.xml
```

## Next Editorial Steps

1. Spot-check raw HTML against the generated TEI.
2. Check footnote targets and duplicate IDs.
3. Refine the semantic structure of the seven meditations.
4. Add German translations section by section.
5. Write meditation texts with clear references to TEI sections.
