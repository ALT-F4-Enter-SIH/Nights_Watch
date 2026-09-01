"""
Stylometry analysis — character n-gram embeddings, Jaccard vocabulary overlap,
punctuation density, average word length.

Lightweight and deterministic; no external model required.
"""
from __future__ import annotations

import re
import string
import math
import time
from collections import Counter
from typing import Dict, List, Tuple

WORD_RE = re.compile(r"[A-Za-z0-9']+")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?")


def _tokenize(text: str) -> List[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def _sentences(text: str) -> List[str]:
    return [s.strip() for s in SENTENCE_RE.findall(text) if s.strip()]


def char_ngrams(text: str, n: int = 3) -> Counter:
    if not text:
        return Counter()
    normalized = re.sub(r"\s+", " ", text.lower())
    return Counter(normalized[i : i + n] for i in range(max(0, len(normalized) - n + 1)))


def writing_signature(text: str) -> Dict[str, float]:
    """Return numeric features that describe writing style."""
    words = _tokenize(text)
    sentences = _sentences(text)
    char_count = max(1, len(text))

    if not words:
        return {
            "avg_word_length": 0.0,
            "punctuation_density": 0.0,
            "vocabulary_diversity": 0.0,
            "sentence_length_avg": 0.0,
            "ngram_signature": {},
        }

    avg_word_length = sum(len(w) for w in words) / len(words)
    punct = sum(1 for c in text if c in string.punctuation)
    punctuation_density = punct / char_count
    unique = set(words)
    vocabulary_diversity = len(unique) / len(words)
    sentence_length_avg = (
        len(words) / max(1, len(sentences)) if sentences else float(len(words))
    )

    ngram_signature = {
        k: round(v / max(1, sum(char_ngrams(text).values())), 6)
        for k, v in char_ngrams(text).most_common(20)
    }

    return {
        "avg_word_length": round(avg_word_length, 3),
        "punctuation_density": round(punctuation_density, 4),
        "vocabulary_diversity": round(vocabulary_diversity, 3),
        "sentence_length_avg": round(sentence_length_avg, 2),
        "ngram_signature": ngram_signature,
    }


def jaccard_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    intersection = sum((a & b).values())
    union = sum((a | b).values())
    return intersection / union if union else 0.0


def cosine_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b.get(k, 0) for k in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def stylometry_similarity(text_a: str, text_b: str) -> Tuple[Dict, Dict, float, int, float, float]:
    sig_a = writing_signature(text_a)
    sig_b = writing_signature(text_b)

    ngrams_a = char_ngrams(text_a)
    ngrams_b = char_ngrams(text_b)
    ngram_score = cosine_similarity(ngrams_a, ngrams_b)

    # Combine features: n-gram cosine is the strongest signal, weighted with style alignment.
    feature_diffs = [
        abs(sig_a["avg_word_length"] - sig_b["avg_word_length"]) / 6.0,
        abs(sig_a["punctuation_density"] - sig_b["punctuation_density"]) / 0.2,
        abs(sig_a["vocabulary_diversity"] - sig_b["vocabulary_diversity"]) / 1.0,
    ]
    style_alignment = max(0.0, 1.0 - sum(feature_diffs) / 3.0)

    similarity = round(0.7 * ngram_score + 0.3 * style_alignment, 4)
    similarity = max(0.0, min(1.0, similarity))

    shared_ngrams = sum(1 for k in (ngrams_a & ngrams_b) if (ngrams_a[k] + ngrams_b[k]) >= 2)
    vocab_a, vocab_b = set(_tokenize(text_a)), set(_tokenize(text_b))
    vocab_union = vocab_a | vocab_b
    vocab_overlap = (
        len(vocab_a & vocab_b) / len(vocab_union) if vocab_union else 0.0
    )
    return sig_a, sig_b, similarity, shared_ngrams, round(vocab_overlap, 3), round(style_alignment, 3)


def measure(start: float | None = None) -> float:
    return round((time.perf_counter() - (start or time.perf_counter())) * 1000, 3)
