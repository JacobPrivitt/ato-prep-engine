from typing import Dict, List, Tuple
from models.artifact import Artifact
from logic.control_catalog import build_control_catalog


def build_artifact_catalog() -> Dict[str, Artifact]:
    artifacts = [
        Artifact(
            artifact_id="SSP",
            name="System Security Plan (SSP)",
            description="System boundary, description, and control implementation narratives (draft is fine).",
            supports_controls=["PL-2"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="POAM",
            name="Plan of Action and Milestones (POA&M)",
            description="Tracks findings, remediation actions, owners, and timelines.",
            supports_controls=["CA-5"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="SAP_SAR",
            name="Assessment Plan and Assessment Report (SAP/SAR)",
            description="Plan how controls are tested and record assessment results.",
            supports_controls=["CA-2"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="NETWORK_DIAGRAM",
            name="Network Diagram",
            description="Logical diagram showing boundary, major components, and external connections.",
            supports_controls=["SC-7"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="ASSET_INVENTORY",
            name="Asset Inventory",
            description="Inventory of hosts, VMs, services, and major software components in scope.",
            supports_controls=["CM-8"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="IR_PLAN",
            name="Incident Response Plan",
            description="IR policy and procedures, roles, escalation, and reporting.",
            supports_controls=["IR-1"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="CONTINGENCY_PLAN",
            name="Contingency Plan",
            description="BCP/DR plan for system availability and recovery procedures.",
            supports_controls=["CP-2"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="VULN_SCAN_RESULTS",
            name="Vulnerability Scan Results",
            description="Scan evidence and remediation tracking, can be Nessus/ACAS or equivalent.",
            supports_controls=["RA-5"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="ACCOUNT_MGMT_SOP",
            name="Account Management SOP",
            description="Provisioning, deprovisioning, privileged access, and periodic review process.",
            supports_controls=["AC-2"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="ACCESS_CONTROL_MATRIX",
            name="Access Control Matrix",
            description="Role-based access mapping for key system roles and permissions.",
            supports_controls=["AC-6"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="SECURITY_PROGRAM_PLAN",
            name="Security Program Plan",
            description="High-level security program governance (lightweight is acceptable for SMB).",
            supports_controls=["PM-1"],
            required_when=["processes_cui"],
        ),
        Artifact(
            artifact_id="CONFIG_BASELINE",
            name="Configuration Baseline",
            description="Baseline configs for servers and key components (what good looks like).",
            supports_controls=["CM-2"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="CONFIG_SETTINGS",
            name="Configuration Settings Standard",
            description="Key security configuration settings and how they are enforced.",
            supports_controls=["CM-6"],
            required_when=["always"],
        ),
        Artifact(
            artifact_id="WINDOWS_STIG_RESULTS",
            name="Windows STIG Results",
            description="STIG checklist or tool output for Windows components in scope.",
            supports_controls=[],
            required_when=["uses_windows"],
        ),
        Artifact(
            artifact_id="LINUX_STIG_RESULTS",
            name="Linux STIG Results",
            description="STIG checklist or tool output for Linux components in scope.",
            supports_controls=[],
            required_when=["uses_linux"],
        ),
        Artifact(
            artifact_id="WEB_STIG_RESULTS",
            name="Web Server STIG Results",
            description="STIG checklist or hardening evidence for the web server stack.",
            supports_controls=[],
            required_when=["uses_web_server"],
        ),
        Artifact(
            artifact_id="DB_STIG_RESULTS",
            name="Database STIG Results",
            description="STIG checklist or hardening evidence for the database stack.",
            supports_controls=[],
            required_when=["uses_database"],
        ),
    ]

    return {a.artifact_id: a for a in artifacts}


def _is_required(tag: str, profile) -> bool:
    if tag == "always":
        return True
    if tag == "uses_windows":
        return bool(getattr(profile, "uses_windows", False))
    if tag == "uses_linux":
        return bool(getattr(profile, "uses_linux", False))
    if tag == "uses_web_server":
        return bool(getattr(profile, "uses_web_server", False))
    if tag == "uses_database":
        return bool(getattr(profile, "uses_database", False))
    if tag == "processes_cui":
        return bool(getattr(profile, "processes_cui", False))
    return False


def required_artifacts_for_profile(profile) -> Tuple[List[Artifact], Dict[str, List[str]]]:
    """
    Returns:
      - list of required Artifact objects
      - dict of artifact_id -> reasons (tags) that made it required
    """
    catalog = build_artifact_catalog()

    required: List[Artifact] = []
    reasons: Dict[str, List[str]] = {}

    for artifact_id, artifact in catalog.items():
        triggered_by = [tag for tag in artifact.required_when if _is_required(tag, profile)]
        if triggered_by:
            required.append(artifact)
            reasons[artifact_id] = triggered_by

    required.sort(key=lambda a: a.artifact_id)
    return required, reasons


def controls_covered_by_artifacts(required_artifacts: List[Artifact]) -> Dict[str, List[str]]:
    """
    Returns dict: control_id -> list of artifact_ids that support it
    """
    coverage: Dict[str, List[str]] = {}
    for art in required_artifacts:
        for ctrl in art.supports_controls:
            coverage.setdefault(ctrl, []).append(art.artifact_id)
    return coverage


def list_controls_missing_evidence(required_artifacts: List[Artifact]) -> List[str]:
    catalog = build_control_catalog()
    coverage = controls_covered_by_artifacts(required_artifacts)

    missing = []
    for control_id in sorted(catalog.keys()):
        if control_id not in coverage:
            missing.append(control_id)
    return missing
