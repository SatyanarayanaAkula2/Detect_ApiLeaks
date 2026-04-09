from config import SEVERITY_MAP
from detector.context import get_context_score

def calculate_risk(secret_type, entropy, context_text):
    base = SEVERITY_MAP.get(secret_type, 5)
    if "TEST" in secret_type:
        return{
            "score":2,
            "risk":"LOW",
            "confidence":0.3,
            "reason":"test key detected"
        }

    if entropy>3.5:
        entropy_score=2
    elif entropy>3:
        entropy_score=1
    else:
        entropy_score=0
    ctx_score=get_context_score(context_text)

    final_score=base + entropy_score + ctx_score
    final_score=max(0,min(final_score,10))

    if(final_score>=8):
        risk="HIGH"
    elif(final_score>=5):
        risk="MEDIUM"   
    elif(final_score>=2):
        risk="LOW"
    else:
        risk="NONE"

    confidence=round((entropy/5)*0.6+(1 if ctx_score>0 else 0.5 if ctx_score==0 else 0.2),2)
    reason=[]
    if entropy>3.5:
        reason.append("high entropy")
    elif entropy>3:
        reason.append("medium entropy")
    if ctx_score>0:
        reason.append("production context")
    elif ctx_score<0:
        reason.append("test context")
    
    if base>=8: reason.append("high severity type")

    return{
        "score":final_score,
        "risk":risk,
        "confidence":confidence,
        "reason":", ".join(reason)
    }