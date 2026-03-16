import socket

import pytest

from dossier.fetching import UnsafeUrlError, _is_disallowed_ip, _validate_public_http_url


def test_is_disallowed_ip() -> None:
    assert _is_disallowed_ip("127.0.0.1") is True
    assert _is_disallowed_ip("10.1.2.3") is True
    assert _is_disallowed_ip("8.8.8.8") is False


def test_validate_public_http_url_rejects_non_http_scheme() -> None:
    with pytest.raises(UnsafeUrlError, match="Unsupported URL scheme"):
        _validate_public_http_url("file:///tmp/test.txt")


def test_validate_public_http_url_rejects_localhost() -> None:
    with pytest.raises(UnsafeUrlError, match="Localhost targets are not allowed"):
        _validate_public_http_url("http://localhost/test")


def test_validate_public_http_url_rejects_private_dns_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_getaddrinfo(
        host: str,
        port: object,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        del host, port, family, type, proto, flags
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.8", 0))]

    monkeypatch.setattr("dossier.fetching.socket.getaddrinfo", fake_getaddrinfo)

    with pytest.raises(UnsafeUrlError, match="non-public IP"):
        _validate_public_http_url("https://example.com/path")


def test_validate_public_http_url_accepts_public_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_getaddrinfo(
        host: str,
        port: object,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> list[tuple[int, int, int, str, tuple[str, int]]]:
        del host, port, family, type, proto, flags
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 0))]

    monkeypatch.setattr("dossier.fetching.socket.getaddrinfo", fake_getaddrinfo)
    _validate_public_http_url("https://example.com")
