from cli.questionnaire import run_questionnaire
from logic.stig_selector import select_stigs
from logic.artifact_mapper import (
    required_artifacts_for_profile,
    controls_covered_by_artifacts,
    list_controls_missing_evidence,
)
from output.exporter import export_package_json, load_package_json
from output.viewer import display_loaded_package


def ask_choice(prompt: str, choices):
    choices_set = set(str(c) for c in choices)
    while True:
        answer = input(prompt).strip()
        if answer in choices_set:
            return answer
        print(f"Please choose one of: {', '.join(sorted(choices_set))}")


def run_new_package_flow():
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

    export_path = export_package_json(
        export_dir="exports",
        profile=profile,
        stigs=stigs,
        required_artifacts=required_artifacts,
        reasons=reasons,
        coverage=coverage,
        missing_controls=missing,
    )

    print(f"\nExported JSON package to: {export_path}")


def run_load_package_flow():
    path = input("\nEnter path to package JSON (example: exports\\package_20260131_123000.json): ").strip().strip('"')
    pkg = load_package_json(path)
    display_loaded_package(pkg)


def main():
    print("=== ATO Prep Engine ===")
    print("1) Create new package")
    print("2) Load existing package JSON")

    choice = ask_choice("Choose 1 or 2: ", choices=["1", "2"])
    if choice == "1":
        run_new_package_flow()
    else:
        run_load_package_flow()


if __name__ == "__main__":
    main()
