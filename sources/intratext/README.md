# IntraText Source

## Source

Work index:

```text
https://www.intratext.com/ixt/itasa0000/_IDX084.HTM
```

The text pages belong to the IntraText collection `ITASA0000`. The downloader uses the hidden-concordance variants `__P*.HTM` so that the TEI conversion is not cluttered by word-level concordance links.

## Download

```sh
python3 scripts/download_intratext.py --fetcher curl --delay 0.5
```

The download writes:

```text
sources/intratext/raw_html/
sources/intratext/manifest.json
```

## License Assumption

IntraText points to its copyright page:

```text
https://www.intratext.com/info/copyENG.htm
```

For now, this project follows the same documented assumption as the sibling project: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported, unless the concrete source states otherwise. This assumption must be checked critically before substantial reuse.
