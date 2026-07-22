import re


def extract_claims(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    sentences = _split_sentences(text.strip())
    claims = []

    for sentence in sentences:
        s = sentence.strip()
        if not s or len(s) < 10:
            continue
        score = _compute_factual_score(s)
        if score >= 3:
            claims.append(s)

    return claims


def compute_confidence(claim_text: str) -> float:
    score = _compute_factual_score(claim_text)
    raw = min(score / 10.0, 1.0)
    return round(max(raw, 0.1), 2)


def classify_initial_status(claim_text: str) -> str:
    return "unreviewed"


def _split_sentences(text: str) -> list[str]:
    pattern = r'(?<=[.!?])\s+(?=[A-Z0-9"“(])'
    parts = re.split(pattern, text)
    return [p.strip() for p in parts if p.strip()]


def _compute_factual_score(sentence: str) -> int:
    score = 0

    patterns = [
        (r'\b(1[89]\d{2}|20\d{2})\b', 3),
        (r'\b\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}\b', 2),
        (r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', 2),
        (r'\b\d+[.,]?\d*\s*(%|percent|million|billion|trillion|kg|km|miles|years|days|hours|people|dollars)\b', 2),
        (r'\b(first|last|largest|smallest|only|best|worst|most|least|tallest|oldest|newest|fastest|slowest)\b', 2),
        (r'\b(according to|reported by|published in|found that|discovered|announced|confirmed|revealed|demonstrated)\b', 2),
        (r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', 2),
        (r'\b[A-Z][a-z]+\s+(?:University|Institute|Corporation|Company|Organization|Foundation|Laboratory)\b', 3),
        (r'\b(is|are|was|were|has been)\s+(?:the|a|an)\b', 1),
        (r'\b(?:more than|less than|approximately|exactly|at least|at most|over|under)\b', 1),
        (r'\b\d+\s*(?:BC|BCE|AD|CE)\b', 3),
        (r'\b(?:won|awarded|received|granted|elected)\b', 2),
        (r'\b(?:caused by|result of|due to|because of|leads to)\b', 1),
        (r'\b\d+°\s*[CF]\b', 2),
    ]

    for pattern, weight in patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            score += weight

    return score


def get_extraction_stats(text: str) -> dict:
    claims = extract_claims(text)
    total_sentences = len(_split_sentences(text))
    return {
        "total_sentences": total_sentences,
        "claims_extracted": len(claims),
        "extraction_rate": round(len(claims) / max(total_sentences, 1) * 100, 1),
    }
