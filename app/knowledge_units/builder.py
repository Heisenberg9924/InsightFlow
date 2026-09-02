from app.knowledge_units.models import KnowledgeUnit
from app.knowledge_units.semantic_chunker import create_knowledge_units
from app.ingestion.sentence_splitter import split_sentences
from app.embeddings.embedder import embed_model

import numpy as np

import re


SENTENCE_ENDINGS = (
    ".",
    "?",
    "!",
    ":",
    ";",
)


def ends_like_complete_sentence(text: str) -> bool:
    """
    Returns True when the block appears to end at a natural
    sentence boundary.
    """

    text = text.strip()

    if not text:
        return True

    # Remove common trailing citation / bracket artifacts.
    cleaned = re.sub(
        r"[\]\)]+$",
        "",
        text,
    ).strip()

    return cleaned.endswith(SENTENCE_ENDINGS)


def starts_like_continuation(text: str) -> bool:
    """
    Detect obvious cases where a new Docling block starts as
    a continuation of the previous block.
    """

    text = text.strip()

    if not text:
        return False

    first_word = text.split()[0]

    # Lowercase beginnings are a very strong signal that this
    # is continuing the previous sentence.
    if first_word[0].islower():
        return True

    continuation_words = {
        "of",
        "and",
        "or",
        "but",
        "while",
        "where",
        "which",
        "that",
        "than",
        "because",
        "although",
        "as",
        "when",
        "whose",
        "whose",
        "with",
        "without",
        "from",
        "to",
    }

    return first_word.lower().strip(
        "([{\"'"
    ) in continuation_words


def should_merge_blocks(
    previous,
    current,
) -> bool:
    """
    Merge only when the previous block appears incomplete
    and the current block clearly begins as its continuation.
    """

    previous_type = previous.block_type.lower()
    current_type = current.block_type.lower()

    # Only merge actual textual content.
    if previous_type not in {
        "text",
        "list_item",
    }:
        return False

    if current_type not in {
        "text",
        "list_item",
    }:
        return False

    previous_text = previous.text.strip()
    current_text = current.text.strip()

    if not previous_text or not current_text:
        return False

    # If A already looks complete, don't merge it.
    if ends_like_complete_sentence(previous_text):
        return False

    # B must look like a continuation.
    if not starts_like_continuation(current_text):
        return False

    return True

def merge_broken_blocks(ordered_blocks):
    """
    Merge obvious cross-block sentence continuations.

    The input must already be in document order.
    """

    merged = []

    for block in ordered_blocks:

        if not merged:
            merged.append(block)
            continue

        previous = merged[-1]

        if should_merge_blocks(
            previous,
            block,
        ):
            previous.text = (
                previous.text.rstrip()
                + " "
                + block.text.lstrip()
            )
        else:
            merged.append(block)

    return merged


def cosine_similarity(a, b):

    a = np.asarray(a)
    b = np.asarray(b)

    denominator = (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(a, b) / denominator
    )


def is_meaningful_text(text: str) -> bool:

    return len(text.split()) >= 4


def build_kus_from_blocks(
    blocks,
    document,
    threshold: float,
):

    knowledge_units = []

    # --------------------------------------------------------------
    # Build blocks in actual Docling document order
    # --------------------------------------------------------------

    ordered_blocks = []

    def collect_blocks(ref):

        block = blocks.get(ref)

        if block is None:
            return

        ordered_blocks.append(block)

        for child_ref in block.children:
            collect_blocks(child_ref)

    for child in document.body.children:
        collect_blocks(child.cref)

    # --------------------------------------------------------------
    # Merge only obvious broken continuations
    # --------------------------------------------------------------

    ordered_blocks = merge_broken_blocks(
        ordered_blocks
    )

    # --------------------------------------------------------------
    # Process blocks
    # --------------------------------------------------------------

    current_heading = None

    for block in ordered_blocks:

        block_type = block.block_type.lower()

        # ----------------------------------------------------------
        # Section heading
        # ----------------------------------------------------------

        if block_type == "section_header":
            current_heading = block.text.strip()
            continue

        # ----------------------------------------------------------
        # Content-bearing blocks
        # ----------------------------------------------------------

        if block_type not in {
            "text",
            "list_item",
        }:
            continue

        text = block.text.strip()

        if not text:
            continue

        if not is_meaningful_text(text):
            continue

        sentences = split_sentences(text)

        if not sentences:
            continue

        metadata = {
            "page": block.page_no,
            "block_type": block.block_type,
            "parent_ref": block.parent_ref,
            "context": current_heading,
        }

        # ----------------------------------------------------------
        # Single sentence
        # ----------------------------------------------------------

        if len(sentences) == 1:

            knowledge_units.append(
                KnowledgeUnit(
                    ku_id=f"{block.ref}_ku_0",
                    parent_id=block.ref,
                    content=sentences[0],
                    metadata=metadata,
                )
            )

            continue

        # ----------------------------------------------------------
        # Multiple sentences
        # ----------------------------------------------------------

        embeddings = [
            embed_model.get_text_embedding(sentence)
            for sentence in sentences
        ]

        similarities = []

        for i in range(len(embeddings) - 1):

            similarities.append(
                cosine_similarity(
                    embeddings[i],
                    embeddings[i + 1],
                )
            )

        kus = create_knowledge_units(
            text=text,
            parent_id=block.ref,
            sentences=sentences,
            similarities=similarities,
            threshold=threshold,
            metadata=metadata,
        )

        knowledge_units.extend(kus)

    return knowledge_units