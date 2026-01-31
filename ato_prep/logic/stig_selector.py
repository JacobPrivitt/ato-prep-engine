def select_stigs(system_profile):
    stigs = []

    if system_profile.uses_windows:
        stigs.append("Windows Server STIG")

    if system_profile.uses_linux:
        stigs.append("RHEL STIG")

    if system_profile.uses_web_server:
        stigs.append("Web Server STIG")

    if system_profile.uses_database:
        stigs.append("Database STIG")

    return stigs
