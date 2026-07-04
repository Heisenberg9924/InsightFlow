from app.models.document import ParsedDocument
from app.processors.cleaner import clean_text
from app.processors.statistics import (
    count_words,
    count_characters,
    count_lines,
    estimate_reading_time,
)


def process_document(document: ParsedDocument) -> ParsedDocument:

    cleaned = clean_text(document.text)

    document.text = cleaned

    document.metadata.word_count = count_words(cleaned)

    document.metadata.extra["character_count"] = count_characters(cleaned)

    document.metadata.extra["line_count"] = count_lines(cleaned)

    document.metadata.extra["estimated_reading_time"] = estimate_reading_time(cleaned)

    return document