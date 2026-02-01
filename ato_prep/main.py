from cli.questionnaire import run_questionnaire
from logic.stig_selector import select_stigs
from logic.artifact_mapper import (
    required_artifacts_for_profile,
    controls_covered_by_artifacts,
    list_controls_missing_evidence,
)
from output.exporter import export_package_json, load_package_json, save_package_json
from output.viewer import display_loaded_package
from logic.readiness_report import print_readiness_report
from logic.migrate import refresh_artifact_mappings



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


from logic.attachments import (
    attach_artifact_file,
    artifact_attachment_status,
    covered_controls_from_attached_artifacts,
)


def run_load_package_flow():
    path = input("\nEnter path to package JSON (example: exports\\package_20260131_123000.json): ").strip().strip('"')
    pkg = load_package_json(path)

    while True:
        display_loaded_package(pkg)

        attached, total = artifact_attachment_status(pkg)
        print(f"\nAttachment Progress: {attached}/{total} artifacts have files attached.")

        evidence_coverage = covered_controls_from_attached_artifacts(pkg)
        print(f"Controls with evidence attached: {len(evidence_coverage)}")

        print("\nOptions:")
        print("1) Attach a file to an artifact")
        print("2) Refresh artifact mappings (apply latest control mappings)")
        print("3) Readiness report")
        print("4) Save package")
        print("5) Save package as (new file)")
        print("6) Exit")

        choice = ask_choice("Choose 1-6: ", choices=["1", "2", "3", "4", "5", "6"])


        if choice == "1":
            artifact_id = input("Enter artifact_id (example: SSP): ").strip()
            file_path = input("Enter file path to attach: ").strip().strip('"')

            updated = attach_artifact_file(pkg, artifact_id, file_path)
            if updated:
                print(f"Attached file to {artifact_id}.")
            else:
                print(f"Artifact ID not found: {artifact_id}")

        elif choice == "2":
            count = refresh_artifact_mappings(pkg)
            print(f"Refreshed mappings for {count} artifacts.")

        elif choice == "3":
            print_readiness_report(pkg, top_missing=10)

        elif choice == "4":
            save_package_json(path, pkg)
            print(f"Saved: {path}")

        elif choice == "5":
            new_path = input("Enter new file path (example: exports\\package_updated.json): ").strip().strip('"')
            save_package_json(new_path, pkg)
            print(f"Saved: {new_path}")

        else:
            break

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
