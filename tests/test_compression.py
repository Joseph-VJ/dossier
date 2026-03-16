from dossier.compression import DemoCompressor, EvidenceCompressor, build_compressor
from dossier.config import Settings
from dossier.contracts import EvidencePacket, SourceAtom


def _packet(index: int, relevance: float, summary: str, quote: str) -> EvidencePacket:
    return EvidencePacket(
        case_id="case_1",
        lane_id="lane_1",
        source_atom=SourceAtom(
            id=f"atom_{index}",
            source_id=f"source_{index}",
            lane_id="lane_1",
            title=f"Source {index}",
            url=f"https://example.com/{index}",
            quote=quote,
            summary=summary,
        ),
        summary=summary,
        quote=quote,
        relevance=relevance,
    )


def test_evidence_compressor_drops_low_relevance_packets() -> None:
    settings = Settings(
        COMPRESSION_MAX_TOKENS_PER_PACKET=100,
        COMPRESSION_MAX_TOTAL_TOKENS=400,
    )
    compressor = EvidenceCompressor(settings)
    packets = [
        _packet(index, relevance=round(1.0 - (index * 0.08), 2), summary="s" * 200, quote="q" * 200)
        for index in range(10)
    ]

    compressed = compressor.compress(packets)

    assert len(compressed) < len(packets)
    assert compressed == sorted(compressed, key=lambda item: item.relevance, reverse=True)


def test_evidence_compressor_truncates_long_packet() -> None:
    settings = Settings(
        COMPRESSION_MAX_TOKENS_PER_PACKET=10,
        COMPRESSION_MAX_TOTAL_TOKENS=400,
    )
    compressor = EvidenceCompressor(settings)
    packet = _packet(1, relevance=0.9, summary="s" * 120, quote="q" * 120)

    [compressed] = compressor.compress([packet])

    assert len(compressed.summary) < len(packet.summary)
    assert len(compressed.quote) < len(packet.quote)
    assert len(compressed.summary) + len(compressed.quote) <= 40


def test_demo_compressor_returns_input_unchanged() -> None:
    packets = [_packet(1, relevance=0.5, summary="summary", quote="quote")]
    assert DemoCompressor().compress(packets) is packets


def test_build_compressor_respects_toggle() -> None:
    enabled = Settings(COMPRESSION_ENABLED=True)
    disabled = Settings(COMPRESSION_ENABLED=False)

    assert isinstance(build_compressor(enabled), EvidenceCompressor)
    assert isinstance(build_compressor(disabled), DemoCompressor)
