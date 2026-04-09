PATTERNS = {
    "AWS_ACCESS_KEY": r"AKIA[0-9A-Z]{16}",
    "OPENAI_KEY": r"sk-[A-Za-z0-9]{40,}",
    "OPENAI_TEST_KEY": r"sk_test_[A-Za-z0-9]{24,}",
    "GITHUB_TOKEN": r"ghp_[A-Za-z0-9]{36}",
    "STRIPE_LIVE_KEY": r"sk_live_[0-9a-zA-Z]{24,}",
    "STRIPE_TEST_KEY": r"sk_test_[0-9a-zA-Z]{24,}",
    "GCP_KEY": r"AIza[0-9A-Za-z\\-_]{35}",
    "PRIVATE_KEY": r"-----BEGIN PRIVATE KEY-----[A-Za-z0-9+/=\s]+-----END PRIVATE KEY-----",
    "BEARER_TOKEN": r"Bearer\s+[A-Za-z0-9\._\-]+",
    "GENERIC_API_KEY": r"(?:api[_-]?key|token|access[_-]?key|secret|password)[=:]?[\"']?([A-Za-z0-9\._\-]{16,})[\"']?"
}

SEVERITY_MAP = {
    "AWS_ACCESS_KEY": 10,
    "PRIVATE_KEY": 10,
    "OPENAI_KEY": 8,
    "STRIPE_LIVE_KEY": 9,
    "GITHUB_TOKEN": 8,
    "STRIPE_KEY": 9,
    "GCP_KEY": 8,
    "STRIPE_TEST_KEY": 2,
    "OPENAI_TEST_KEY": 2,
    "BEARER_TOKEN": 7,
    "GENERIC_API_KEY": 6

}

LOW_RISK_WORDS = ["test", "dummy", "sample", "example","mock","fake","dev","staging","sandbox"]
HIGH_RISK_WORDS = ["prod", "live", "production", "secret", "private", "key", "token"]

WIN_SECRET_LENGTH=16
CONTEXT_WINDOW=50

ENTROPY_THRESHOLD={
    "low":3.0,
    "medium":4.0
}