from typing import Dict
from models.control import Control


def build_control_catalog() -> Dict[str, Control]:
    controls = [
        Control("PM-1", "Information Security Program Plan", "PM", ["SECURITY_PROGRAM_PLAN"]),
        Control("PL-2", "System Security Plan", "PL", ["SSP"]),
        Control("CA-2", "Control Assessments", "CA", ["SAP_SAR"]),
        Control("CA-5", "Plan of Action and Milestones", "CA", ["POAM"]),
        Control("CM-2", "Baseline Configuration", "CM", ["CONFIG_BASELINE"]),
        Control("CM-6", "Configuration Settings", "CM", ["CONFIG_SETTINGS"]),
        Control("AC-2", "Account Management", "AC", ["ACCOUNT_MGMT_SOP"]),
        Control("AC-6", "Least Privilege", "AC", ["ACCESS_CONTROL_MATRIX"]),
        Control("IR-1", "Incident Response Policy and Procedures", "IR", ["IR_PLAN"]),
        Control("CP-2", "Contingency Plan", "CP", ["CONTINGENCY_PLAN"]),
        Control("RA-5", "Vulnerability Monitoring and Scanning", "RA", ["VULN_SCAN_RESULTS"]),
        Control("SC-7", "Boundary Protection", "SC", ["NETWORK_DIAGRAM"]),
        Control("CM-8", "System Component Inventory", "CM", ["ASSET_INVENTORY"]),
    ]

    return {c.control_id: c for c in controls}
