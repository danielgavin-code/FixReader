"""
Lightweight internal-link crawler for FIXReader.

Uses the Flask test client — no real web server required.
Returns a CrawlResult with every URL visited and every failure found,
including the page that contained the broken link.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Optional
from urllib.parse import urlparse, urljoin

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# ---------------------------------------------------------------------------
# HTML link extractor
# ---------------------------------------------------------------------------

class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        d = dict(attrs)
        # Page links and stylesheet references
        if tag == 'a':
            self._add(d.get('href', ''))
        elif tag == 'link':
            self._add(d.get('href', ''))
        # Script and image src
        elif tag in ('script', 'img'):
            self._add(d.get('src', ''))
        # Form actions
        elif tag == 'form':
            self._add(d.get('action', ''))

    def _add(self, val: str):
        if val:
            self.links.append(val)


def _extract_links(html: str) -> list[str]:
    p = _LinkParser()
    p.feed(html)
    return p.links


# ---------------------------------------------------------------------------
# URL classification helpers
# ---------------------------------------------------------------------------

_SKIP_SCHEMES = {'mailto', 'javascript', 'data', 'http', 'https', 'tel', 'ftp'}


def _should_skip(href: str) -> bool:
    """True for external, mailto:, javascript:, data:, fragment-only, etc."""
    if not href or href.startswith('#'):
        return True
    parsed = urlparse(href)
    return parsed.scheme in _SKIP_SCHEMES


def _normalize(path: str) -> str:
    """Strip fragment and trailing query string noise, keep path + query."""
    parsed = urlparse(path)
    out = parsed.path
    if parsed.query:
        out += '?' + parsed.query
    return out


# ---------------------------------------------------------------------------
# Tag numbers that are valid in the app (for filtering intentional 404s)
# ---------------------------------------------------------------------------

def _valid_tag_numbers() -> set[int]:
    try:
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'fixreader_data', 'fix_tags.json',
        )
        with open(data_dir) as f:
            return {t['tag'] for t in json.load(f)}
    except Exception:
        return set()


def _is_intentional_tag_gap(path: str, valid_tags: set[int]) -> bool:
    """Tag-navigation prev/next links can point to tag numbers not in the DB.
    These render a graceful 404 stub — not a site error."""
    parts = path.strip('/').split('/')
    if len(parts) == 2 and parts[0] == 'tag' and parts[1].isdigit():
        return int(parts[1]) not in valid_tags
    return False


# ---------------------------------------------------------------------------
# Crawl result
# ---------------------------------------------------------------------------

@dataclass
class Failure:
    source: str       # page that contained the link
    target: str       # URL that failed
    status: int       # HTTP status code
    note: str = ''    # optional context


@dataclass
class CrawlResult:
    visited: list[str] = field(default_factory=list)
    failures: list[Failure] = field(default_factory=list)

    def ok(self) -> bool:
        return len(self.failures) == 0

    def failure_report(self) -> str:
        lines = []
        for f in self.failures:
            lines.append(
                f'Broken internal link:\n'
                f'  Source: {f.source}\n'
                f'  Target: {f.target}\n'
                f'  Status: {f.status}'
                + (f'\n  Note:   {f.note}' if f.note else '')
            )
        return '\n\n'.join(lines)


# ---------------------------------------------------------------------------
# Crawler
# ---------------------------------------------------------------------------

# Routes that are intentionally guarded / POST-only / not crawlable
_SKIP_PATHS = {
    '/decode',                  # POST-only API
    '/themes-admin',            # guarded by ENABLE_THEME_ADMIN
    '/themes-admin/apply',      # POST-only
    '/themes-admin/edit',       # POST-only
}

# Valid reference versions
_REFERENCE_VERSIONS = [
    'fix40', 'fix41', 'fix42', 'fix43',
    'fix44', 'fix50', 'fix50sp1', 'fix50sp2',
]


def crawl(client, extra_seeds: Optional[list[str]] = None) -> CrawlResult:
    """
    Crawl all internal links reachable from '/' plus a set of known seed paths
    that are only reachable via JS-rendered navigation.

    Parameters
    ----------
    client : Flask test client
    extra_seeds : additional paths to seed (default: reference pages, static files)
    """
    valid_tags = _valid_tag_numbers()

    # Seed: homepage + route families not reachable via HTML links alone
    seeds: list[tuple[str, str]] = [('/', 'seed')]
    for ver in _REFERENCE_VERSIONS:
        seeds.append((f'/reference/{ver}', 'seed'))
    seeds += [
        ('/static/css/main.css', 'seed'),
        ('/static/js/search.js', 'seed'),
    ]
    if extra_seeds:
        for s in extra_seeds:
            seeds.append((s, 'seed'))

    result = CrawlResult()
    seen: set[str] = set()
    queue: list[tuple[str, str]] = list(seeds)  # (path, source)

    while queue:
        raw_path, source = queue.pop(0)
        path = _normalize(raw_path)

        if not path or path in seen:
            continue
        seen.add(path)

        if _should_skip(path):
            continue

        # Strip query for skip-path check
        base_path = path.split('?')[0]
        if base_path in _SKIP_PATHS:
            continue

        r = client.get(path, follow_redirects=False)
        result.visited.append(path)
        status = r.status_code

        # Handle redirects: record destination and continue crawling there
        if status in (301, 302):
            loc = r.headers.get('Location', '')
            if loc:
                loc_norm = _normalize(loc)
                if not _should_skip(loc_norm) and loc_norm not in seen:
                    queue.append((loc_norm, path))
                # Verify the redirect destination is reachable
                dest = client.get(loc, follow_redirects=True)
                if dest.status_code not in (200, 301, 302, 404):
                    result.failures.append(Failure(
                        source=source,
                        target=path,
                        status=dest.status_code,
                        note=f'redirect destination {loc} returned {dest.status_code}',
                    ))
            continue

        # Flag unexpected status codes
        if status == 404:
            # Tag-navigation gaps are intentional — not a site failure
            if not _is_intentional_tag_gap(base_path, valid_tags):
                result.failures.append(Failure(
                    source=source, target=path, status=404
                ))
            continue

        if status >= 400:
            result.failures.append(Failure(
                source=source, target=path, status=status
            ))
            continue

        # Only parse HTML responses for further links
        ct = r.content_type or ''
        if 'html' not in ct:
            continue

        html = r.data.decode('utf-8', errors='ignore')
        for raw_link in _extract_links(html):
            if _should_skip(raw_link):
                continue
            # Resolve relative to current path (most links are absolute anyway)
            link_path = _normalize(raw_link if raw_link.startswith('/') else raw_link)
            if link_path and link_path not in seen:
                queue.append((link_path, path))

    return result
