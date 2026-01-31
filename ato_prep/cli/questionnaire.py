from models.system_profile import SystemProfile


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def run_questionnaire() -> SystemProfile:
    print("\n=== System Questionnaire ===\n")

    profile = SystemProfile()

    profile.uses_windows = ask_yes_no("Does the system use Windows?")
    profile.uses_linux = ask_yes_no("Does the system use Linux?")
    profile.uses_web_server = ask_yes_no("Does the system have a web server?")
    profile.uses_database = ask_yes_no("Does the system use a database?")
    profile.processes_cui = ask_yes_no("Does the system process CUI?")

    return profile
