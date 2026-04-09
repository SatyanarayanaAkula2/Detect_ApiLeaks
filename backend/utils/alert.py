def send_alert(finding):
    """simulate sending an alert to developer
    """
    repo=finding.get("source", "unknown repo")
    type=finding.get("type", "unknown type")
    risk=finding.get("risk", "unknown risk")
    reason=finding.get("reason", "unknown reason")

    alert_message=f"""
!SECURITY ALERT!
Repository:{repo}
Secret Type:{type}
Risk Level:{risk}
Reason:{reason}

Action Required:
-Revoke the key immediately
-Rotate credentials
-Remove from source code
"""
    print(alert_message)
    return alert_message
