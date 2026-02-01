from typing import Any, Dict

from logic.artifact_mapper import build_artifact_catalog


def refresh_artifact_mappings(pkg: Dict[str, Any]) -> int:
    """
    Updates artifacts in a loaded JSON package using the current artifact catalog.
    Returns the count of artifacts updated.
    """
    catalog = build_artifact_catalog()
    updated = 0

    artifacts = pkg.get("required_artifacts", [])
    for a in artifacts:
        artifact_id = a.get("artifact_id")
        if not artifact_id:
            continue

        if artifact_id in catalog:
            cat = catalog[artifact_id]
            # Update fields we want to keep current
            a["name"] = cat.name
            a["description"] = cat.description
            a["supports_controls"] = list(cat.supports_controls)
            updated += 1

    return updated
