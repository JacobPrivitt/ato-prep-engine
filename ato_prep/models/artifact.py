from dataclasses import dataclass, field
from typing import List


@dataclass
class Artifact:
    artifact_id: str             # "SSP"
    name: str                    # "System Security Plan (SSP)"
    description: str
    supports_controls: List[str] = field(default_factory=list)
    required_when: List[str] = field(default_factory=list)
    # required_when is simple tags like:
    # "always", "uses_windows", "uses_linux", "uses_web_server", "uses_database", "processes_cui"
