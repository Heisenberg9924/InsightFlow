import spacy


# Lightweight English pipeline.
nlp = spacy.blank("en")

# Rule-based sentence boundary detection.
nlp.add_pipe("sentencizer")


def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    if not text or not text.strip():
        return []

    doc = nlp(text)

    return [
        sentence.text.strip()
        for sentence in doc.sents
        if sentence.text.strip()
    ]