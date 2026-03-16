from __future__ import annotations

from pathlib import Path

from dossier.contracts import (
    EvidencePacket,
    InvestigationMetrics,
    InvestigationPlan,
    RankedInsight,
    TriggerResult,
)


def _append_bullet_section(lines: list[str], heading: str, items: list[str]) -> None:
    lines.append(heading)
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append("- None recorded.")
    lines.append("")


def render_dossier_markdown(
    question: str,
    case_id: str,
    plan: InvestigationPlan,
    packets: list[EvidencePacket],
    triggers: list[TriggerResult],
    insights: list[RankedInsight],
    metrics: InvestigationMetrics,
) -> str:
    lines = [
        f"# Dossier: {question}",
        "",
        f"- Case ID: `{case_id}`",
        f"- Objective: {plan.objective}",
        f"- Novelty target: {plan.novelty_target}",
        "",
        "## Research Lanes",
    ]

    for lane in plan.lanes:
        lines.extend(
            [
                f"### {lane.name}",
                f"- Query: `{lane.query}`",
                f"- Goal: {lane.goal}",
                "",
            ]
        )

    lines.append("## Evidence Packets")
    for packet in packets:
        lines.extend(
            [
                f"### {packet.source_atom.title}",
                f"- Lane: `{packet.lane_id}`",
                f"- Source atom: `{packet.source_atom.id}`",
                f"- URL: {packet.source_atom.url}",
                f"- Summary: {packet.summary}",
                f"- Quote: {packet.quote}",
                "",
            ]
        )

    lines.append("## Trigger Detection")
    if triggers:
        for trigger in triggers:
            lines.extend(
                [
                    f"### {trigger.trigger_type.value}",
                    f"- Description: {trigger.description}",
                    f"- Confidence: {trigger.confidence}",
                    f"- Supporting evidence: {', '.join(trigger.supporting_evidence) or 'None'}",
                    "",
                ]
            )
    else:
        lines.extend(["- No triggers fired.", ""])

    lines.append("## Ranked Insights")
    for insight in insights:
        lines.extend(
            [
                f"### {insight.title}",
                f"- Class: {insight.insight_class.value}",
                f"- Score: {insight.score.total}",
                "- Score breakdown:",
                f"  - NoveltyDistance: {insight.score.novelty_distance}",
                f"  - SynthesisDepth: {insight.score.synthesis_depth}",
                f"  - MechanismQuality: {insight.score.mechanism_quality}",
                f"  - PredictivePower: {insight.score.predictive_power}",
                f"  - CrossDomainTransfer: {insight.score.cross_domain_transfer}",
                f"  - TokenEfficiency: {insight.score.token_efficiency}",
                f"  - CoherencePenalty: {insight.score.coherence_penalty}",
                f"- Summary: {insight.summary}",
                f"- Source atoms: {', '.join(insight.source_atoms)}",
                f"- Assumptions: {', '.join(insight.assumptions)}",
                f"- Disconfirming signals: {', '.join(insight.disconfirming_signals)}",
                "",
                f"Mechanism: {insight.mechanism.name}",
                insight.mechanism.description,
            ]
        )
        _append_bullet_section(lines, "Mechanism steps:", insight.mechanism.steps)
        lines.extend(
            [
                "Proof Tree:",
                f"- Conclusion: {insight.proof_tree.conclusion}",
            ]
        )
        _append_bullet_section(lines, "Premises:", insight.proof_tree.premises)
        _append_bullet_section(lines, "Reasoning notes:", insight.proof_tree.reasoning_notes)
        for prediction in insight.predicted_observables:
            lines.append(
                f"- Prediction: {prediction.observable} -> {prediction.expected_signal} "
                f"({prediction.time_horizon}, confidence {prediction.confidence})"
            )
        lines.append("")
        if insight.counterfactual_tests:
            lines.append("Counterfactual tests:")
            for index, test in enumerate(insight.counterfactual_tests, start=1):
                lines.extend(
                    [
                        f"- Test {index} assumption: {test.assumption}",
                        f"  - Challenge prompt: {test.challenge_prompt}",
                        f"  - Expected failure mode: {test.expected_failure_mode}",
                    ]
                )
            lines.append("")

    lines.extend(
        [
            "## Metrics",
            f"- Search queries: {metrics.search_queries}",
            f"- Sources considered: {metrics.sources_considered}",
            f"- Evidence packets: {metrics.evidence_packets}",
            f"- Packets after compression: {metrics.packets_after_compression}",
            f"- Evidence atoms extracted: {metrics.evidence_atoms_extracted}",
            f"- Graph nodes created: {metrics.graph_nodes_created}",
            f"- Graph edges created: {metrics.graph_edges_created}",
            f"- Triggers fired: {metrics.triggers_fired}",
            f"- Trigger types: {', '.join(metrics.trigger_types) if metrics.trigger_types else 'None'}",
            f"- Synthesis mode: {metrics.synthesis_mode}",
            f"- Tokens in: {metrics.tokens_in}",
            f"- Tokens out: {metrics.tokens_out}",
            f"- Estimated cost USD: {metrics.estimated_cost_usd}",
            f"- Latency seconds: {metrics.latency_seconds}",
            f"- Grounded novelty ratio: {metrics.grounded_novelty_ratio}",
            f"- Coherence failures: {metrics.coherence_failures}",
            "",
        ]
    )
    return "\n".join(lines)


def write_dossier(output_dir: Path, case_id: str, content: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    dossier_path = output_dir / f"{case_id}.md"
    dossier_path.write_text(content, encoding="utf-8")
    return dossier_path
