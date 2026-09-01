from typing import List, Dict, Tuple


def exact_username_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    if id1.get("username") == id2.get("username"):
        return True, 1.0, "Exact username match"
    return False, 0.0, ""


def fuzzy_alias_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    aliases1 = set(str(a).lower() for a in id1.get("aliases", []))
    aliases2 = set(str(a).lower() for a in id2.get("aliases", []))
    common = aliases1.intersection(aliases2)
    if common:
        score = min(0.95, 0.5 + 0.2 * len(common))
        return True, score, f"Shared aliases: {', '.join(common)}"
    for a1 in aliases1:
        for a2 in aliases2:
            if a1 in a2 or a2 in a1:
                return True, 0.75, f"Similar alias: {a1} / {a2}"
    return False, 0.0, ""


def pgp_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    fp1 = id1.get("pgp_fingerprint") or ""
    fp2 = id2.get("pgp_fingerprint") or ""
    if fp1 and fp2 and fp1 == fp2:
        return True, 1.0, "Exact PGP fingerprint match"
    if fp1 and fp2:
        fp1_short = fp1[-16:] if len(fp1) >= 16 else fp1
        fp2_short = fp2[-16:] if len(fp2) >= 16 else fp2
        if fp1_short == fp2_short:
            return True, 0.85, "PGP short key ID match"
    return False, 0.0, ""


def crypto_wallet_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    w1 = set(str(w).lower() for w in id1.get("crypto_wallets", []))
    w2 = set(str(w).lower() for w in id2.get("crypto_wallets", []))
    common = w1.intersection(w2)
    if common:
        return True, 1.0, f"Shared wallet: {', '.join(common)}"
    return False, 0.0, ""


def behavioral_pattern_match(id1: Dict, id2: Dict) -> Tuple[bool, float, str]:
    cats1 = set(str(c).lower() for c in id1.get("categories", []))
    cats2 = set(str(c).lower() for c in id2.get("categories", []))
    common_cats = cats1.intersection(cats2)
    hours1 = set(id1.get("posting_hours", []))
    hours2 = set(id2.get("posting_hours", []))
    common_hours = hours1.intersection(hours2)
    score = 0.0
    evidence = []
    if common_cats:
        score += 0.3
        evidence.append(f"Shared categories: {len(common_cats)}")
    if common_hours:
        score += 0.4
        evidence.append(f"Shared posting hours: {len(common_hours)}")
    return score > 0, min(0.8, score), "; ".join(evidence) if evidence else ""


def run_correlation(id1: Dict, id2: Dict) -> List[Dict]:
    relations = []
    for fn, label in [
        (exact_username_match, "username"),
        (fuzzy_alias_match, "alias"),
        (pgp_match, "pgp"),
        (crypto_wallet_match, "crypto"),
        (behavioral_pattern_match, "behavioral"),
    ]:
        match, score, explanation = fn(id1, id2)
        if match:
            relations.append({
                "correlation_type": label,
                "confidence_score": score,
                "evidence": {"method": label},
                "explanation": explanation,
            })
    return relations
