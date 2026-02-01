import json
import os
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, List


def _to_jsonable(obj: Any) -> Any:
    """
    Convert objects (including dataclasses) into JSON-serializable structures.
    """
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, list):
        return [_to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    # Fallback: try using __dict__
    if hasattr(obj, "__dict__"):
        return {k: _to_jsonable(v) for k, v in obj.__dict__.items()}
    return str(obj)


def export_package_json(
    export_dir: str,
    profile,
    stigs: List[str],
    required_artifacts,
    reasons: Dict[str, List[str]],
    coverage: Dict[str, List[str]],
    missing_controls: List[str],
) -> str:
    """
    Writes a JSON file and returns the path.
    """
    os.makedirs(export_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"package_{timestamp}.json"
    path = os.path.join(export_dir, filename)

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "system_profile": _to_jsonable(profile),
        "prescribed_stigs": stigs,
        "required_artifacts": [
            {
                **_to_jsonable(art),
                "required_reasons": reasons.get(getattr(art, "artifact_id", ""), []),
            }
            for art in required_artifacts
        ],
        "control_coverage": coverage,
        "missing_controls": missing_controls,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path
