import re
from config import PATTERNS

def detect_secrets(text):
    findings = []

    for key_type, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)

        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            findings.append({
                "secret": match,
                "type": key_type
            })

    return findings