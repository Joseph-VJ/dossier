from __future__ import annotations

import logging
from typing import Protocol

from dossier.config import Settings
from dossier.contracts import EvidencePacket

logger = logging.getLogger(__name__)


class Compressor(Protocol):
    def compress(self, packets: list[EvidencePacket]) -> list[EvidencePacket]:
        ...


class EvidenceCompressor:
    def __init__(self, settings: Settings) -> None:
        self.max_chars_per_packet = max(1, settings.compression_max_tokens_per_packet) * 4
        self.max_total_tokens = max(1, settings.compression_max_total_tokens)

    def compress(self, packets: list[EvidencePacket]) -> list[EvidencePacket]:
        truncated_chars = 0
        truncated_packets = [self._truncate_packet(packet) for packet in packets]
        for original, truncated in zip(packets, truncated_packets, strict=False):
            truncated_chars += (
                len(original.summary) + len(original.quote) - len(truncated.summary) - len(truncated.quote)
            )

        kept_packets: list[EvidencePacket] = []
        dropped_packets = 0
        used_tokens = 0
        for packet in sorted(truncated_packets, key=lambda item: item.relevance, reverse=True):
            packet_tokens = self._estimate_tokens(packet)
            if used_tokens + packet_tokens > self.max_total_tokens:
                dropped_packets += 1
                continue
            kept_packets.append(packet)
            used_tokens += packet_tokens

        logger.info(
            "Compression kept %s/%s packets, dropped %s, truncated %s chars",
            len(kept_packets),
            len(packets),
            dropped_packets,
            truncated_chars,
        )
        return kept_packets

    def _truncate_packet(self, packet: EvidencePacket) -> EvidencePacket:
        combined_length = len(packet.summary) + len(packet.quote)
        if combined_length <= self.max_chars_per_packet:
            return packet

        summary_budget = max(12, int(self.max_chars_per_packet * 0.6))
        quote_budget = max(12, self.max_chars_per_packet - summary_budget)
        return packet.model_copy(
            update={
                "summary": self._truncate_text(packet.summary, summary_budget),
                "quote": self._truncate_text(packet.quote, quote_budget),
            }
        )

    def _truncate_text(self, value: str, limit: int) -> str:
        if len(value) <= limit:
            return value
        if limit <= 3:
            return value[:limit]
        return f"{value[: limit - 3]}..."

    def _estimate_tokens(self, packet: EvidencePacket) -> int:
        return max(1, (len(packet.summary) + len(packet.quote)) // 4)


class DemoCompressor:
    def compress(self, packets: list[EvidencePacket]) -> list[EvidencePacket]:
        return packets


def build_compressor(settings: Settings) -> Compressor:
    if settings.compression_enabled:
        return EvidenceCompressor(settings)
    return DemoCompressor()
