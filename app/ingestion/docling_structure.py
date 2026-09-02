from dataclasses import dataclass, field
from typing import Optional


SEMANTIC_BLOCK_TYPES = {
    "text",
    "list_item",
}

ATOMIC_BLOCK_TYPES = {
    "code",
    "formula",
    "table",
    "picture",
    "list",
    "section_header",
    "footnote",
    "caption",
}

MIN_WORDS = 4


@dataclass
class StructuralBlock:
    ref: str
    block_type: str
    text: str
    parent_ref: Optional[str] = None
    page_no: Optional[int] = None
    level: Optional[int] = None
    children: list[str] = field(default_factory=list)


def is_semantic_candidate(
    block: StructuralBlock,
) -> bool:

    block_type = block.block_type.lower()

    if block_type not in SEMANTIC_BLOCK_TYPES:
        return False

    words = block.text.split()

    return len(words) >= MIN_WORDS


def extract_docling_structure(document):

    blocks = {}

    # --------------------------------------------------------------
    # Extract text blocks
    # --------------------------------------------------------------

    for item in document.texts:

        ref = item.self_ref

        parent_ref = (
            item.parent.cref
            if item.parent is not None
            else None
        )

        page_no = None

        if item.prov:
            page_no = item.prov[0].page_no

        blocks[ref] = StructuralBlock(
            ref=ref,
            block_type=item.label.value,
            text=item.text,
            parent_ref=parent_ref,
            page_no=page_no,
            level=getattr(item, "level", None),
        )

    # --------------------------------------------------------------
    # Extract groups
    # --------------------------------------------------------------

    for group in document.groups:

        ref = group.self_ref

        parent_ref = (
            group.parent.cref
            if group.parent is not None
            else None
        )

        children = [
            child.cref
            for child in group.children
        ]

        blocks[ref] = StructuralBlock(
            ref=ref,
            block_type=group.label.value,
            text="",
            parent_ref=parent_ref,
            children=children,
        )

    return blocks


def print_block(
    ref,
    blocks,
    indent=0,
):

    block = blocks.get(ref)

    if block is None:
        return

    prefix = " " * indent

    print(
        f"{prefix}[{block.block_type.upper()}]"
        f"{block.ref}"
    )

    if block.text:
        print(
            f"{prefix} {block.text}"
        )

    if block.page_no is not None:
        print(
            f"{prefix} page = {block.page_no}"
        )

    for child_ref in block.children:

        print_block(
            child_ref,
            blocks,
            indent + 1,
        )


def print_structure(
    blocks,
    document,
):

    print("=" * 80)
    print("DOCLING STRUCTURE")
    print("=" * 80)

    for child in document.body.children:

        print_block(
            child.cref,
            blocks,
            indent=0,
        )


def classify_blocks(blocks):

    candidates = []
    atomic = []

    for block in blocks.values():

        if is_semantic_candidate(block):
            candidates.append(block)

        else:
            atomic.append(block)

    return candidates, atomic