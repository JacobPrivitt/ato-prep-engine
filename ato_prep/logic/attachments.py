from typing import Any, Dict, List, Tuple


def list_artifacts(pkg: Dict[str, Any]) -> List[Dict[str, Any]]:
    return pkg.get("required_artifacts", [])


def attach_artifact_file(pkg: Dict[str, Any], artifact_id: str, file_path: str) -> bool:
    """
    Attaches file_path to the artifact with artifact_id.
    Returns True if updated, False if artifact_id not found.
    """
    artifacts = list_artifacts(pkg)
    for a in artifacts:
        if a.get("artifact_id") == artifact_id:
            a["attached_file"] = file_path
            return True
    return False


def artifact_attachment_status(pkg: Dict[str, Any]) -> Tuple[int, int]:
    """
    Returns (attached_count, total_count)
    """
    artifacts = list_artifacts(pkg)
    total = len(artifacts)
    attached = 0
    for a in artifacts:
        if a.get("attached_file"):
            attached += 1
    return attached, total


def covered_controls_from_attached_artifacts(pkg: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Computes control coverage based only on artifacts that have an attached file.
    Returns dict: control_id -> list of artifact_ids that provide evidence.
    """
    coverage: Dict[str, List[str]] = {}
    artifacts = list_artifacts(pkg)
    for a in artifacts:
        if not a.get("attached_file"):
            continue
        aid = a.get("artifact_id", "UNKNOWN")
        supports = a.get("supports_controls", [])
        for ctrl in supports:
            coverage.setdefault(ctrl, []).append(aid)
    return coverage
