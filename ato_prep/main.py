from cli.questionnaire import run_questionnaire
from logic.stig_selector import select_stigs


def main():
    profile = run_questionnaire()

    print("\nSystem Profile Summary:")
    print(profile.summary())

    stigs = select_stigs(profile)

    print("\nPrescribed STIGs:")
    for stig in stigs:
        print(f"- {stig}")


if __name__ == "__main__":
    main()
