"""Word Sense Disambiguation using WordNet and NLTK's simplified Lesk baseline."""
import re
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

PUNCT = ".,!?;:'\"()[]{}"

def ensure_wordnet():
    try:
        wn.synsets("test")
    except LookupError as exc:
        raise RuntimeError(
            "WordNet data is missing. Run: python -m nltk.downloader wordnet omw-1.4"
        ) from exc

def clean_token(token):
    return token.lower().strip(PUNCT)

def get_word_senses(sentence, target_word):
    """Return candidate senses and the simplified Lesk prediction for one target word."""
    ensure_wordnet()
    target = clean_token(target_word)
    words = [clean_token(w) for w in sentence.split()]
    if target not in words:
        return {"error": f'The target word "{target_word}" was not found in the sentence.', "senses": []}

    synsets = wn.synsets(target)
    senses = []
    for syn in synsets[:15]:
        senses.append({
            "name": syn.name(),
            "part_of_speech": syn.pos(),
            "definition": syn.definition(),
            "examples": syn.examples()[:2],
            "lemmas": [lemma.name().replace("_", " ") for lemma in syn.lemmas()[:8]],
            "hypernyms": [h.name().split(".")[0].replace("_", " ") for h in syn.hypernyms()[:4]],
        })

    predicted = lesk(sentence.split(), target)
    predicted_info = None
    if predicted:
        predicted_info = {
            "name": predicted.name(),
            "definition": predicted.definition(),
            "part_of_speech": predicted.pos(),
            "lemmas": [lemma.name().replace("_", " ") for lemma in predicted.lemmas()[:8]],
            "examples": predicted.examples()[:2],
        }
    return {
        "sentence": sentence,
        "target_word": target_word,
        "predicted": predicted_info,
        "senses": senses,
        "candidate_count": len(synsets),
    }

def analyze_sentence(sentence: str, target_word: str) -> dict:
    sentence = sentence.strip()
    target_word = target_word.strip()
    if not sentence or not target_word:
        return {"error": "Enter both a sentence and a target word.", "senses": []}
    result = get_word_senses(sentence, target_word)
    result["note"] = "Simplified Lesk is a baseline and may predict the wrong sense. Review the candidates in context."
    return result

def analyze_all_ambiguous_words(sentence: str, max_words: int = 12) -> dict:
    """Find distinct words with multiple WordNet senses and analyze each."""
    ensure_wordnet()
    tokens = re.findall(r"[A-Za-z][A-Za-z'-]*", sentence)
    seen, candidates = set(), []
    for token in tokens:
        word = clean_token(token)
        if len(word) < 3 or word in seen:
            continue
        seen.add(word)
        senses = wn.synsets(word)
        if len(senses) > 1:
            candidates.append(word)
        if len(candidates) >= max_words:
            break
    results = []
    for word in candidates:
        item = get_word_senses(sentence, word)
        if not item.get("error"):
            results.append(item)
    return {
        "sentence": sentence,
        "results": results,
        "word_count": len(tokens),
        "unique_words": len(set(clean_token(t) for t in tokens)),
        "ambiguous_count": len(results),
        "note": f"Showing up to {max_words} distinct words with multiple WordNet senses. This is a candidate list, not a guarantee that each word is ambiguous in this context.",
    }
