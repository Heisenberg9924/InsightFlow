import re


def count_words(text: str) -> int:
    return len(text.split())


def count_characters(text: str) -> int:
    return len(text)


def count_lines(text: str) -> int:
    return len(text.splitlines())


def estimate_reading_time(text: str) -> float:
    """
    Reading speed ≈ 200 words/minute.
    """
    words = count_words(text)
    return round(words / 200, 2)