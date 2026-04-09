from datetime import datetime

def mask(secret):
    return secret[:4] + "****" + secret[-4:]


def timestamp():
    return datetime.utcnow().isoformat()