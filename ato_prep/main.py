from models.system_profile import SystemProfile
from logic.stig_selector import select_stigs


def main():
    profile = SystemProfile()
    profile.uses_windows = True
    profile.uses_web_server = True
    profile.processes_cui = True

    print("System Profile:")
    print(profile.summary())

    stigs = select_stigs(profile)

    print("\nPrescribed STIGs:")
    for stig in stigs:
        print(f"- {stig}")


if __name__ == "__main__":
    main()
