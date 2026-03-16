from __future__ import annotations

import ipaddress
import re
import socket
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from readability import Document


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


class UnsafeUrlError(ValueError):
    """Raised when a URL points to a non-public destination."""


def _is_disallowed_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def _validate_public_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        msg = f"Unsupported URL scheme for fetch: {parsed.scheme or '<none>'}"
        raise UnsafeUrlError(msg)

    host = parsed.hostname
    if not host:
        msg = "URL must include a valid hostname."
        raise UnsafeUrlError(msg)

    normalized_host = host.strip(".").lower()
    if normalized_host in {"localhost", "localhost.localdomain"}:
        msg = "Localhost targets are not allowed."
        raise UnsafeUrlError(msg)

    if _is_disallowed_ip(normalized_host):
        msg = f"Blocked non-public host IP: {normalized_host}"
        raise UnsafeUrlError(msg)

    try:
        resolved = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        msg = f"Could not resolve host for fetch: {host}"
        raise UnsafeUrlError(msg) from exc

    for result in resolved:
        resolved_ip_raw = result[4][0]
        if not isinstance(resolved_ip_raw, str):
            continue
        resolved_ip = resolved_ip_raw
        if _is_disallowed_ip(resolved_ip):
            msg = f"Blocked host resolved to non-public IP: {resolved_ip}"
            raise UnsafeUrlError(msg)


@dataclass(frozen=True)
class FetchedPage:
    url: str
    title: str
    content: str
    excerpt: str


class HttpFetcher:
    def __init__(self, max_redirects: int = 5) -> None:
        self.max_redirects = max_redirects

    def fetch(self, url: str) -> FetchedPage:
        current_url = url
        headers = {"User-Agent": "dossier/0.1 (+local investigation scaffold)"}
        for _ in range(self.max_redirects + 1):
            _validate_public_http_url(current_url)
            response = httpx.get(
                current_url,
                timeout=20.0,
                follow_redirects=False,
                headers=headers,
            )

            if 300 <= response.status_code < 400 and "location" in response.headers:
                current_url = urljoin(str(response.url), response.headers["location"])
                continue

            response.raise_for_status()
            break
        else:
            msg = f"Too many redirects while fetching {url}"
            raise UnsafeUrlError(msg)

        html = response.text
        document = Document(html)
        summary_html = document.summary()
        title = document.short_title() or str(response.url)
        soup = BeautifulSoup(summary_html or html, "html.parser")
        text = _collapse_whitespace(soup.get_text(" ", strip=True))
        excerpt = text[:280]
        return FetchedPage(url=str(response.url), title=title, content=text[:8000], excerpt=excerpt)
