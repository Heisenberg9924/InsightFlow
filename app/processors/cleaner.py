import re
import unicodedata


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters into a consistent form.
    """
    return unicodedata.normalize("NFKC", text)


def remove_extra_whitespace(text: str) -> str:
    """
    Replace multiple spaces/tabs with a single space.
    """
    return re.sub(r"[ \t]+", " ", text)


def remove_extra_newlines(text: str) -> str:
    """
    Collapse multiple blank lines into a single blank line.
    """
    return re.sub(r"\n{3,}", "\n\n", text)


def clean_text(text: str) -> str:
    """
    Run all cleaning steps.
    """
    text = normalize_unicode(text)
    text = remove_extra_whitespace(text)
    text = remove_extra_newlines(text)

    return text.strip()