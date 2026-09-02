"""
Comprehensive AI Stylometry Engine for writing style comparison.

Implements advanced text similarity analysis using:
- TF-IDF Vectorization
- Cosine Similarity
- N-gram analysis
- Sentence structure analysis
- Punctuation pattern analysis
- Semantic similarity with sentence embeddings
- Combined scoring for final stylometric similarity
"""
from __future__ import annotations

import re
import string
from collections import Counter
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
from math import sqrt

# Initialize sentence transformer for semantic similarity
try:
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    SEMANTIC_MODEL_AVAILABLE = True
except:
    SEMANTIC_MODEL_AVAILABLE = False
    print("Warning: SentenceTransformer not available - semantic similarity will be limited")


def tokenize(text: str) -> List[str]:
    """Tokenize text into words."""
    # Remove punctuation but keep it for later analysis
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.lower().split()


def get_word_frequencies(text: str) -> Counter:
    """Get word frequency counts."""
    words = tokenize(text)
    return Counter(words)


def get_sentence_structure(text: str) -> Dict:
    """Analyze sentence structure."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return {
            'avg_sentence_length': 0.0,
            'sentence_count': 0,
            'avg_words_per_sentence': 0.0,
            'long_sentences': 0,
            'short_sentences': 0
        }

    sentence_lengths = [len(s.split()) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    avg_words_per_sentence = avg_sentence_length
    long_sentences = sum(1 for length in sentence_lengths if length > 15)
    short_sentences = sum(1 for length in sentence_lengths if length <= 5)

    return {
        'avg_sentence_length': round(avg_sentence_length, 2),
        'sentence_count': len(sentences),
        'avg_words_per_sentence': round(avg_words_per_sentence, 2),
        'long_sentences': long_sentences,
        'short_sentences': short_sentences
    }


def punctuation_analysis(text: str) -> Dict:
    """Analyze punctuation patterns."""
    # Count different types of punctuation
    punct_counts = Counter()
    for char in text:
        if char in string.punctuation:
            punct_counts[char] += 1

    # Calculate punctuation density
    char_count = len(text)
    if char_count == 0:
        punct_density = 0.0
    else:
        punct_density = sum(punct_counts.values()) / char_count

    # Analyze punctuation distribution
    punct_types = {
        '.': 'period',
        ',': 'comma',
        '!': 'exclamation',
        '?': 'question',
        ';': 'semicolon',
        ':': 'colon',
        "'": 'apostrophe',
        '"': 'quotation'
    }

    punct_categories = Counter()
    for char in text:
        if char in string.punctuation:
            cat = punct_types.get(char, 'other')
            categories[cat] += 1

    return {
        'punctuation_density': round(punct_density, 4),
        'punctuation_distribution': dict(categories.items()) if 'categories' in locals() else {},
        'most_common_punct': punct_counts.most_common(3) if punct_counts else []
    }


def compute_tfidf_similarity(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts."""
    # Handle empty texts
    if not text_a or not text_b:
        return 0.0

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=1,
        max_df=0.9
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception:
        return 0.0


def compute_semantic_similarity(text_a: str, text_b: str) -> float:
    """Compute semantic similarity using sentence embeddings."""
    if not SEMANTIC_MODEL_AVAILABLE:
        return 0.5  # Default if model not available

    if not text_a or not text_b:
        return 0.5  # Neutral similarity for empty texts

    try:
        # Get embeddings
        embeddings_a = sentence_model.encode([text_a])
        embeddings_b = sentence_model.encode([text_b])

        # Calculate cosine similarity
        similarity = cosine_similarity(embeddings_a[0].reshape(1, -1), embeddings_b[0].reshape(1, -1))[0][0]
        return float(similarity)
    except Exception:
        return 0.5


def compute_sentence_structure_similarity(text_a: str, text_b: str) -> float:
    """Compute similarity in sentence structure."""
    struct_a = get_sentence_structure(text_a)
    struct_b = get_sentence_structure(text_b)

    if struct_a['sentence_count'] == 0 or struct_b['sentence_count'] == 0:
        return 0.0

    # Compare key structural features
    score = 0.0

    # Sentence count similarity (normalized)
    sentence_count_diff = abs(struct_a['sentence_count'] - struct_b['sentence_count'])
    max_count = max(struct_a['sentence_count'], struct_b['sentence_count'])
    sentence_count_score = 1.0 - (sentence_count_diff / max_count) if max_count > 0 else 1.0
    score += sentence_count_score * 0.3

    # Average sentence length similarity
    length_diff = abs(struct_a['avg_sentence_length'] - struct_b['avg_sentence_length'])
    max_length = max(struct_a['avg_sentence_length'], struct_b['avg_sentence_length'])
    if max_length > 0:
        length_score = 1.0 - (length_diff / max_length)
    else:
        length_score = 1.0
    score += length_score * 0.3

    # Word count per sentence similarity
    words_diff = abs(struct_a['avg_words_per_sentence'] - struct_b['avg_words_per_sentence'])
    max_words = max(struct_a['avg_words_per_sentence'], struct_b['avg_words_per_sentence'])
    if max_words > 0:
        words_score = 1.0 - (words_diff / max_words)
    else:
        words_score = 1.0
    score += words_score * 0.2

    # Sentence length distribution similarity
    long_diff = abs(struct_a['long_sentences'] - struct_b['long_sentences'])
    short_diff = abs(struct_a['short_sentences'] - struct_b['short_sentences'])
    distribution_score = 1.0 - ((long_diff + short_diff) / (struct_a['sentence_count'] + struct_b['sentence_count']) if struct_a['sentence_count'] + struct_b['sentence_count'] > 0 else 1.0)
    score += distribution_score * 0.2

    return min(1.0, score)


def compute_punctuation_similarity(text_a: str, text_b: str) -> float:
    """Compute similarity in punctuation patterns."""
    punct_a = punctuation_analysis(text_a)
    punct_b = punctuation_analysis(text_b)

    if not punct_a or not punct_b:
        return 0.0

    # Compare punctuation density
    density_diff = abs(punct_a['punctuation_density'] - punct_b['punctuation_density'])
    max_density = max(punct_a['punctuation_density'], punct_b['punctuation_density'])
    if max_density > 0:
        density_score = 1.0 - (density_diff / max_density)
    else:
        density_score = 1.0

    # Compare most common punctuation
    common_punct_a = set(punct_a['most_common_punct']) if punct_a['most_common_punct'] else set()
    common_punct_b = set(punct_b['most_common_punct']) if punct_b['most_common_punct'] else set()
    common_punct_score = len(common_punct_a & common_punct_b) / max(len(common_punct_a), len(common_punct_b), 1)

    # Overall punctuation similarity
    score = (density_score * 0.6 + common_punct_score * 0.4)
    return min(1.0, score)


def compute_n_gram_similarity(text_a: str, text_b: str) -> float:
    """Compute n-gram similarity using character n-grams."""
    def get_ngrams(text: str, n: int = 3) -> List[str]:
        text = re.sub(r'\s+', ' ', text.lower())
        return [text[i:i+n] for i in range(max(0, len(text) - n + 1))]

    ngrams_a = get_ngrams(text_a, 3)
    ngrams_b = get_ngrams(text_b, 3)

    if not ngrams_a or not ngrams_b:
        return 0.0

    # Count n-grams
    counter_a = Counter(ngrams_a)
    counter_b = Counter(ngrams_b)

    # Calculate intersection
    common_ngrams = counter_a & counter_b
    if not common_ngrams:
        return 0.0

    # Jaccard similarity
    intersection = sum(common_ngrams.values())
    union = sum(counter_a.values()) + sum(counter_b.values()) - intersection
    return intersection / union if union > 0 else 0.0


def compute_overall_stylometry_similarity(text_a: str, text_b: str) -> Dict:
    """Compute comprehensive stylometry similarity score."""
    # Handle edge cases
    if not text_a or not text_b:
        return {
            'similarity_score': 0.0,
            'tfidf_similarity': 0.0,
            'semantic_similarity': 0.0,
            'sentence_structure_similarity': 0.0,
            'punctuation_similarity': 0.0,
            'ngram_similarity': 0.0,
            'features': [],
            'explanation': 'One or both texts are empty'
        }

    # Calculate individual similarity signals
    tfidf_sim = compute_tfidf_similarity(text_a, text_b)
    semantic_sim = compute_semantic_similarity(text_a, text_b)
    sentence_struct_sim = compute_sentence_structure_similarity(text_a, text_b)
    punct_sim = compute_punctuation_similarity(text_a, text_b)
    ngram_sim = compute_n_gram_similarity(text_a, text_b)

    # Combine signals with weighted average (weights can be adjusted)
    # Based on typical importance in stylometry
    weights = {
        'tfidf_similarity': 0.25,
        'semantic_similarity': 0.25,
        'sentence_structure_similarity': 0.20,
        'punctuation_similarity': 0.15,
        'ngram_similarity': 0.15
    }

    total_weight = sum(weights.values())
    overall_score = 0.0
    for key in weights:
        if key == 'tfidf_similarity':
            overall_score += weights[key] * tfidf_sim
        elif key == 'semantic_similarity':
            overall_score += weights[key] * semantic_sim
        elif key == 'sentence_structure_similarity':
            overall_score += weights[key] * sentence_struct_sim
        elif key == 'punctuation_similarity':
            overall_score += weights[key] * punct_sim
        elif key == 'ngram_similarity':
            overall_score += weights[key] * ngram_sim

    # Ensure score is between 0 and 1
    overall_score = max(0.0, min(1.0, overall_score))

    # Generate features list
    features = []
    if tfidf_sim > 0.7:
        features.append("High TF-IDF overlap")
    elif tfidf_sim > 0.5:
        features.append("Moderate TF-IDF overlap")

    if semantic_sim > 0.7:
        features.append("Strong semantic similarity")
    elif semantic_sim > 0.5:
        features.append("Moderate semantic similarity")

    if sentence_struct_sim > 0.7:
        features.append("Similar sentence structure")
    elif sentence_struct_sim > 0.5:
        features.append("Similar sentence structure patterns")

    if punct_sim > 0.7:
        features.append("Similar punctuation usage")
    elif punct_sim > 0.5:
        features.append("Similar punctuation patterns")

    if ngram_sim > 0.7:
        features.append("Strong n-gram overlap")
    elif ngram_sim > 0.5:
        features.append("Moderate n-gram similarity")

    # Create explanation
    explanation_parts = []
    explanation_parts.append(f"TF-IDF similarity: {tfidf_sim:.2f}")
    explanation_parts.append(f"Semantic similarity: {semantic_sim:.2f}")
    explanation_parts.append(f"Sentence structure similarity: {sentence_struct_sim:.2f}")
    explanation_parts.append(f"Punctuation similarity: {punct_sim:.2f}")
    explanation_parts.append(f"N-gram similarity: {ngram_sim:.2f}")
    explanation_parts.append(f"Overall stylometry score: {overall_score:.2f}")

    if features:
        explanation_parts.append("Key features: " + "; ".join(features))
    else:
        explanation_parts.append("No significant stylistic differences detected")

    explanation = " ".join(explanation_parts)

    return {
        'similarity_score': round(overall_score * 100, 2),
        'signals': {
            'tfidf_similarity': round(tfidf_sim * 100, 2),
            'semantic_similarity': round(semantic_sim * 100, 2),
            'sentence_structure_similarity': round(sentence_struct_sim * 100, 2),
            'punctuation_similarity': round(punct_sim * 100, 2)
        },
        'matching_features': features,
        'explanation': explanation
    }


def measure(text: str) -> float:
    """Measure text characteristics."""
    return len(text) if text else 0


if __name__ == "__main__":
    # Simple test
    text1 = "The quick brown fox jumps over the lazy dog. This is a sample text."
    text2 = "A quick brown fox leaps over a sleepy dog. Here is another example text."

    result = compute_overall_stylometry_similarity(text1, text2)
    print("Stylometry Analysis:")
    print(f"  Overall similarity: {result['similarity_score']}%")
    print("  Signals:")
    for key, value in result['signals'].items():
        print(f"    {key}: {value}%")
    print("  Features:", result['matching_features'])
    print("  Explanation:", result['explanation'])