from cli.questionnaire import run_questionnaire
from logic.stig_selector import select_stigs
from logic.artifact_mapper import (
    required_artifacts_for_profile,
    controls_covered_by_artifacts,
    list_controls_missing_evidence,
)


def main():
    profile = run_questionnaire()

    print("\nSystem Profile Summary:")
    print(profile.summary())

    stigs = select_stigs(profile)
    print("\nPrescribed STIGs:")
    for stig in stigs:
        print(f"- {stig}")

    required_artifacts, reasons = required_artifacts_for_profile(profile)

    print("\nRequired Artifacts:")
    for art in required_artifacts:
        reason_str = ", ".join(reasons.get(art.artifact_id, []))
        print(f"\n[{art.artifact_id}] {art.name}")
        print(f"Reason: {reason_str}")
        print(f"Description: {art.description}")
        if art.supports_controls:
            print("Supports controls: " + ", ".join(art.supports_controls))
        else:
            print("Supports controls: (none mapped yet)")

    coverage = controls_covered_by_artifacts(required_artifacts)
    print("\nControl Coverage Summary:")
    for ctrl_id in sorted(coverage.keys()):
        print(f"- {ctrl_id}: {', '.join(coverage[ctrl_id])}")

    missing = list_controls_missing_evidence(required_artifacts)
    if missing:
        print("\nControls missing direct evidence mapping (expected early on):")
        for ctrl_id in missing:
            print(f"- {ctrl_id}")
    else:
        print("\nAll controls have at least one supporting artifact.")


if __name__ == "__main__":
    main()
