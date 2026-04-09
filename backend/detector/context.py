from config import LOW_RISK_WORDS, HIGH_RISK_WORDS,CONTEXT_WINDOW

def extract_context(text, secret):
    idx = text.find(secret)
    if(idx==-1):
        return ""
    return text[max(0, idx-CONTEXT_WINDOW): idx+len(secret)+CONTEXT_WINDOW]


def get_context_score(context):
    context=context.lower()
    score = 0

    for word in LOW_RISK_WORDS:
        if word in context:
            score -= 2

    for word in HIGH_RISK_WORDS:
        if word in context:
            score += 3

    return score