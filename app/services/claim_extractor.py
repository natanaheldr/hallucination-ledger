import re


def extract_claims(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    claims = []

    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        if _is_factual(s):
            claims.append(s)

    return claims if claims else []


def _is_factual(sentence: str) -> bool:
    if len(sentence) < 10:
        return False

    score = 0

    if re.search(r'\b(19|20)\d{2}\b', sentence):
        score += 3

    if re.search(r'\b\d+[\.,]?\d*\s*(%|percent|million|billion|trillion|kg|km|miles|years|days|hours)\b', sentence, re.IGNORECASE):
        score += 2

    if re.search(r'\b(is|are|was|were|has|have|had)\b', sentence, re.IGNORECASE):
        score += 1

    if re.search(r'\b(first|last|largest|smallest|only|best|worst|most|least|tallest|oldest|newest)\b', sentence, re.IGNORECASE):
        score += 2

    if re.search(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', sentence):
        score += 2

    if re.search(r'\b(according to|reported|published|found that|discovered|announced)\b', sentence, re.IGNORECASE):
        score += 2

    if re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', sentence):
        score += 2

    if re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', sentence):
        score += 2

    return score >= 3


def classify_initial_status(claim_text: str) -> str:
    return "unreviewed"
