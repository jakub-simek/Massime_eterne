#!/usr/bin/env python3
"""Download the IntraText HTML source pages for Massime eterne."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import ssl
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://www.intratext.com/ixt/itasa0000/"
INDEX_PATH = "_IDX084.HTM"
INDEX_URL = urljoin(BASE_URL, INDEX_PATH)
OUT_DIR = Path("sources/intratext")
RAW_DIR = OUT_DIR / "raw_html"
MANIFEST = OUT_DIR / "manifest.json"
USER_AGENT = "Massime-eterne-TEI/0.1 (+noncommercial scholarly edition)"


@dataclass
class DownloadedPage:
    order: int
    kind: str
    title: str
    source_url: str
    local_path: str
    bytes: int
    sha256: str


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_dict = {name.lower(): value for name, value in attrs if value is not None}
        href = attrs_dict.get("href")
        if href:
            self._current_href = href
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current_href:
            title = " ".join("".join(self._current_text).split())
            self.links.append({"href": self._current_href, "title": html.unescape(title)})
            self._current_href = None
            self._current_text = []


def fetch(url: str, *, insecure_tls: bool = False, fetcher: str = "urllib") -> bytes:
    if fetcher == "curl":
        command = [
            "curl",
            "--silent",
            "--show-error",
            "--location",
            "--max-time",
            "60",
            "--user-agent",
            USER_AGENT,
            url,
        ]
        if insecure_tls:
            command.insert(1, "--insecure")
        completed = subprocess.run(command, check=True, capture_output=True)
        return completed.stdout

    request = Request(url, headers={"User-Agent": USER_AGENT})
    context = ssl._create_unverified_context() if insecure_tls else None
    with urlopen(request, timeout=30, context=context) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean_text_page_url(href: str) -> str:
    """Convert `_P2HQ.HTM` to `__P2HQ.HTM`."""
    url = urljoin(BASE_URL, href)
    parsed = urlparse(url)
    filename = Path(parsed.path).name
    if re.fullmatch(r"_P[0-9A-Z]+\.HTM", filename, flags=re.IGNORECASE):
        clean_filename = "_" + filename
        return urljoin(url, clean_filename)
    return url


def local_name_for(url: str) -> str:
    filename = Path(urlparse(url).path).name
    return filename.lower()


def collect_pages(index_html: bytes) -> list[dict[str, str]]:
    parser = LinkCollector()
    parser.feed(index_html.decode("iso-8859-1", errors="replace"))

    pages: list[dict[str, str]] = []
    seen: set[str] = set()

    for link in parser.links:
        href = link["href"]
        filename = Path(urlparse(href).path).name
        if not re.fullmatch(r"_P[0-9A-Z]+\.HTM", filename, flags=re.IGNORECASE):
            continue
        source_url = clean_text_page_url(href)
        if source_url in seen:
            continue
        seen.add(source_url)
        pages.append(
            {
                "kind": "text",
                "title": link["title"],
                "source_url": source_url,
            }
        )

    return pages


def write_page(
    page: dict[str, str],
    order: int,
    delay: float,
    insecure_tls: bool,
    fetcher: str,
) -> DownloadedPage:
    url = page["source_url"]
    data = fetch(url, insecure_tls=insecure_tls, fetcher=fetcher)
    local_path = RAW_DIR / local_name_for(url)
    local_path.write_bytes(data)
    if delay:
        time.sleep(delay)
    return DownloadedPage(
        order=order,
        kind=page["kind"],
        title=page["title"],
        source_url=url,
        local_path=str(local_path),
        bytes=len(data),
        sha256=sha256(data),
    )


def build_manifest(pages: Iterable[DownloadedPage], index_page: DownloadedPage) -> dict:
    return {
        "work": {
            "title": "Massime eterne",
            "subtitle": "cioe meditazioni per ciascun giorno della settimana",
            "author": "S. Alfonso Maria de Liguori",
            "intratext_id": "ITASA0000",
            "intratext_work_index": INDEX_PATH,
            "index_url": INDEX_URL,
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "source_note": "Text pages use IntraText's hidden-concordance-link variant (__P*.HTM).",
            "print_source": "S. Alfonso Maria de Liguori, OPERE ASCETICHE, Vol. IX, pp. 381-395, Edizioni di Storia e Letteratura, Roma 1965.",
            "electronic_transcription": "P. Salvatore Brugnano, CSSR",
            "markup": "EuloTech ETML",
            "license": "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported, unless otherwise noted",
            "license_url": "https://www.intratext.com/info/copyENG.htm",
        },
        "index": asdict(index_page),
        "pages": [asdict(page) for page in pages],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between page requests in seconds.")
    parser.add_argument(
        "--insecure-tls",
        action="store_true",
        help="Disable TLS certificate verification. Use only when the local Python certificate store is broken.",
    )
    parser.add_argument(
        "--fetcher",
        choices=["urllib", "curl"],
        default="urllib",
        help="HTTP client used for downloads.",
    )
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    index_data = fetch(INDEX_URL, insecure_tls=args.insecure_tls, fetcher=args.fetcher)
    index_local = RAW_DIR / INDEX_PATH.lower()
    index_local.write_bytes(index_data)
    index_page = DownloadedPage(
        order=0,
        kind="index",
        title="Indice opera",
        source_url=INDEX_URL,
        local_path=str(index_local),
        bytes=len(index_data),
        sha256=sha256(index_data),
    )

    page_specs = collect_pages(index_data)
    downloaded = [
        write_page(page, i, args.delay, args.insecure_tls, args.fetcher)
        for i, page in enumerate(page_specs, start=1)
    ]

    manifest = build_manifest(downloaded, index_page)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Downloaded {len(downloaded)} text pages plus index.")
    print(f"Wrote {MANIFEST}.")


if __name__ == "__main__":
    main()
