from typing import Any, Dict, List


def _safe_get(d: Dict[str, Any], key: str, default):
    val = d.get(key, default)
    return val if val is not None else default


def display_loaded_package(pkg: Dict[str, Any]) -> None:
    print("\n=== Loaded Package Summary ===")

    generated_at = pkg.get("generated_at", "unknown")
    print(f"Generated at: {generated_at}")

    profile = pkg.get("system_profile", {})
    print("\nSystem Profile:")
    # Print whatever exists, future-proof
    for k in sorted(profile.keys()):
        print(f"- {k}: {profile[k]}")

    stigs: List[str] = pkg.get("prescribed_stigs", [])
    print("\nPrescribed STIGs:")
    if stigs:
        for s in stigs:
            print(f"- {s}")
    else:
        print("(none)")

    artifacts = pkg.get("required_artifacts", [])
    print("\nRequired Artifacts:")
    if artifacts:
        for a in artifacts:
            aid = a.get("artifact_id", "UNKNOWN")
            name = a.get("name", "Unnamed Artifact")
            reasons = a.get("required_reasons", [])
            print(f"\n[{aid}] {name}")
            if reasons:
                print("Reason: " + ", ".join(reasons))
            desc = a.get("description", "")
            if desc:
                print(f"Description: {desc}")
            supports = a.get("supports_controls", [])
            if supports:
                print("Supports controls: " + ", ".join(supports))
    else:
        print("(none)")

    coverage = pkg.get("control_coverage", {})
    print("\nControl Coverage Summary:")
    if coverage:
        for ctrl_id in sorted(coverage.keys()):
            print(f"- {ctrl_id}: {', '.join(coverage[ctrl_id])}")
    else:
        print("(none)")

    missing = pkg.get("missing_controls", [])
    print("\nMissing Controls:")
    if missing:
        for ctrl_id in missing:
            print(f"- {ctrl_id}")
    else:
        print("(none)")
