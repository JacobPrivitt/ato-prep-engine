class SystemProfile:
    def __init__(self):
        self.uses_windows = False
        self.uses_linux = False
        self.uses_database = False
        self.uses_web_server = False
        self.processes_cui = False

    def summary(self) -> str:
        return (
            f"Windows: {self.uses_windows}, "
            f"Linux: {self.uses_linux}, "
            f"Database: {self.uses_database}, "
            f"Web Server: {self.uses_web_server}, "
            f"CUI: {self.processes_cui}"
        )
