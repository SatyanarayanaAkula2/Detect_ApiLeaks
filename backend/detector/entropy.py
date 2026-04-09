import math
from collections import Counter

def shannon_entropy(data):
    if not data:
        return 0

    freq = Counter(data)
    probs = [v / len(data) for v in freq.values()]

    return -sum(p * math.log2(p) for p in probs)