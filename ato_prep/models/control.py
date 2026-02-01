from dataclasses import dataclass, field
from typing import List


@dataclass
class Control:
    control_id: str              # "AC-2"
    title: str                   # "Account Management"
    family: str                  # "AC"
    required_artifacts: List[str] = field(default_factory=list)
