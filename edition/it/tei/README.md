# Italian TEI Text

## Generation

```sh
python3 scripts/convert_intratext_to_tei.py
```

Input:

```text
sources/intratext/manifest.json
sources/intratext/raw_html/
```

Output:

```text
edition/it/tei/massime-eterne.xml
```

## Current Mapping

- IntraText pages are emitted as `<div type="...">`.
- Printed pages are preserved as `<pb n="..."/>`.
- IntraText page boundaries are preserved as `<milestone unit="intratext-page">`.
- Footnote references are emitted as `<ref type="note" target="#note-...">`.
- Footnotes are collected in the back matter under `<back>`.

## Limits

The current file is a conservative first-pass conversion. The internal structure of the seven meditations still needs editorial review and semantic refinement.
