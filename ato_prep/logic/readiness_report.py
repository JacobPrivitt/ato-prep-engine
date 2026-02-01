from typing import Any, Dict, List, Tuple

from logic.attachments import artifact_attachment_status, covered_controls_from_attached_artifacts
from logic.control_catalog import build_control_catalog


def _recommended_artifacts_for_control(pkg: Dict[str, Any], control_id: str) -> List[str]:
    """
    Look through the package's required_artifacts list and find artifacts that support control_id.
    """
    rec = []
    for a in pkg.get("required_artifacts", []):
        supports = a.get("supports_controls", [])
        if control_id in supports:
            rec.append(a.get("artifact_id", "UNKNOWN"))
    return sorted(set(rec))


def generate_readiness_summary(pkg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a structured readiness summary dict.
    """
    control_catalog = build_control_catalog()
    total_controls = len(control_catalog)

    attached_count, total_artifacts = artifact_attachment_status(pkg)

    evidence_coverage = covered_controls_from_attached_artifacts(pkg)
    covered_controls = sorted(evidence_coverage.keys())
    covered_count = len(covered_controls)

    missing_controls = sorted([cid for cid in control_catalog.keys() if cid not in evidence_coverage])

    missing_details = []
    for cid in missing_controls:
        missing_details.append(
            {
                "control_id": cid,
                "title": control_catalog[cid].title,
                "recommended_artifacts": _recommended_artifacts_for_control(pkg, cid),
            }
        )

    return {
        "artifact_progress": {
            "attached": attached_count,
            "total": total_artifacts,
            "percent": (attached_count / total_artifacts * 100.0) if total_artifacts else 0.0,
        },
        "control_progress": {
            "covered": covered_count,
            "total": total_controls,
            "percent": (covered_count / total_controls * 100.0) if total_controls else 0.0,
        },
        "controls_with_evidence": covered_controls,
        "missing_controls": missing_details,
    }


def print_readiness_report(pkg: Dict[str, Any], top_missing: int = 10) -> None:
    summary = generate_readiness_summary(pkg)

    ap = summary["artifact_progress"]
    cp = summary["control_progress"]

    print("\n=== Readiness Report ===")
    print(f"Artifacts attached: {ap['attached']}/{ap['total']} ({ap['percent']:.1f}%)")
    print(f"Controls with evidence: {cp['covered']}/{cp['total']} ({cp['percent']:.1f}%)")

    # What to do next
    missing = summary["missing_controls"]
    if not missing:
        print("\nAll catalog controls have evidence attached. (Nice.)")
        return

    print(f"\nTop {min(top_missing, len(missing))} missing controls to address next:")
    for item in missing[:top_missing]:
        cid = item["control_id"]
        title = item["title"]
        rec = item["recommended_artifacts"]

        print(f"\n- {cid} — {title}")
        if rec:
            print("  Recommended artifacts to attach: " + ", ".join(rec))
        else:
            print("  Recommended artifacts to attach: (none in current required set)")
            print("  Note: this likely means the artifact catalog needs expansion for this control.")
