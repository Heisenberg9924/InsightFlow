import json
import os

from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GENAI_API_KEY"),
)


MODEL = "gemini-2.5-flash"

BATCH_SIZE = 10

OUTPUT_PATH = Path(
    "data/continuity_analysis.json"
)


@dataclass
class ContinuityDecision:
    continue_text: bool
    reason: str


class LLMDecision(BaseModel):
    pair_id: int
    decision: str
    reason: str


class BatchDecision(BaseModel):
    decisions: list[LLMDecision]
    
    
CONTINUITY_PROMPT = """
You are a document reconstruction system.

You are given multiple pairs of adjacent TEXT blocks extracted from
the same document.

For every pair, determine whether BLOCK B is a continuation of
BLOCK A that was separated because of document layout, pagination,
column extraction, or another extraction artifact.

IMPORTANT DISTINCTION:

"Related" does NOT mean "continuation".

Two blocks may discuss the exact same topic and still need to remain
separate if they are independently complete sentences or paragraphs.

Return CONTINUE ONLY when there is strong evidence that:

1. BLOCK B grammatically continues BLOCK A, OR
2. joining A and B produces one coherent sentence or passage that
   appears to have been broken by document layout or extraction.

Return SEPARATE when:

1. BLOCK A is already a complete sentence or paragraph and BLOCK B
   starts a new sentence or paragraph.
2. A and B are merely related or discuss the same concept.
3. A and B belong to the same section but represent different ideas.
4. B appears to be a new heading, label, caption, metadata item,
   example, or independent statement.

Examples:

A:
"The output is computed as a weighted sum"

B:
"of the values, where the weight assigned to each value..."

CONTINUE


A:
"The Transformer uses self-attention."

B:
"The encoder contains six identical layers."

SEPARATE


A:
"Attention mechanisms allow dependencies regardless of distance."

B:
"This makes them useful for sequence transduction."

SEPARATE


A:
"The output is computed as a weighted sum,"

B:
"where the weight assigned to each value is computed by a
compatibility function."

CONTINUE


A:
"The encoder maps the input sequence to representations."

B:
"The decoder then generates the output sequence."

SEPARATE


Be conservative.

When uncertain, choose SEPARATE.

Return exactly one decision for every pair.

Allowed decisions:

CONTINUE
SEPARATE
"""

def llm_continuity_batch(pairs):
    """
    Ask Gemini to classify multiple adjacent TEXT pairs
    in a single request.
    """

    formatted_pairs = []

    for pair_id, previous, current in pairs:

        formatted_pairs.append(
            f"""
PAIR {pair_id}

BLOCK A:
{previous.text}

BLOCK A TYPE:
{previous.block_type}

BLOCK A PAGE:
{previous.page_no}

BLOCK B:
{current.text}

BLOCK B TYPE:
{current.block_type}

BLOCK B PAGE:
{current.page_no}
"""
        )

    prompt = (
        CONTINUITY_PROMPT
        + "\n\n"
        + "\n".join(formatted_pairs)
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json",
            "response_schema": BatchDecision,
        },
    )
    if response.parsed is not None:
      return response.parsed.decisions


def needs_continuity_check(
    previous_text: str,
) -> bool:

    text = previous_text.rstrip()

    if not text:
        return False

    # Clearly unfinished punctuation.
    if text[-1] in {
        ",",
        ":",
        ";",
        "-",
        "—",
        "(",
        "[",
    }:
        return True

    # No obvious terminal punctuation.
    if text[-1] not in {
        ".",
        "?",
        "!",
    }:
        return True

    return False

def build_pairs(blocks):

    text_blocks = [
        block
        for block in blocks.values()
        if (
            block.block_type.lower() == "text"
            and block.text.strip()
        )
    ]

    pairs = []

    for i in range(len(text_blocks) - 1):

        previous = text_blocks[i]
        current = text_blocks[i + 1]

        if needs_continuity_check(previous.text):

            pairs.append(
                (
                    len(pairs),
                    previous,
                    current,
                )
            )

    return text_blocks, pairs

def load_existing_results():

    if not OUTPUT_PATH.exists():
        return {}

    with OUTPUT_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    return {
        result["pair_id"]: result
        for result in data.get("results", [])
    }
    
    
def save_results(
    text_blocks,
    results,
):

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ordered_results = sorted(
        results.values(),
        key=lambda x: x["pair_id"],
    )

    output = {
        "num_text_blocks": len(text_blocks),
        "num_pairs_analyzed": len(ordered_results),
        "num_continue": sum(
            r["decision"] == "CONTINUE"
            for r in ordered_results
        ),
        "num_separate": sum(
            r["decision"] == "SEPARATE"
            for r in ordered_results
        ),
        "results": ordered_results,
    }

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )
        
def analyze_text_continuity(blocks):

    text_blocks, pairs = build_pairs(blocks)

    existing = load_existing_results()

    print(
        f"Text blocks: {len(text_blocks)}"
    )

    print(
        f"Potential continuity pairs: {len(pairs)}"
    )

    print(
        f"Already analyzed: {len(existing)}"
    )

    remaining = [
        pair
        for pair in pairs
        if pair[0] not in existing
    ]

    print(
        f"Remaining: {len(remaining)}"
    )

    for start in range(
        0,
        len(remaining),
        BATCH_SIZE,
    ):

        batch = remaining[
            start:start + BATCH_SIZE
        ]

        print()
        print(
            f"Processing batch "
            f"{start // BATCH_SIZE + 1}"
        )

        decisions = llm_continuity_batch(
            batch
        )

        decision_map = {
            decision.pair_id: decision
            for decision in decisions
        }

        for pair_id, previous, current in batch:

            decision = decision_map.get(
                pair_id
            )

            if decision is None:
                raise RuntimeError(
                    f"Missing decision for pair "
                    f"{pair_id}"
                )

            normalized = decision.decision.upper()

            if normalized not in {
                "CONTINUE",
                "SEPARATE",
            }:
                raise ValueError(
                    f"Invalid decision for pair "
                    f"{pair_id}: {normalized}"
                )

            existing[pair_id] = {
                "pair_id": pair_id,

                "previous_ref": previous.ref,
                "current_ref": current.ref,

                "previous_text": previous.text,
                "current_text": current.text,

                "previous_page": previous.page_no,
                "current_page": current.page_no,

                "decision": normalized,
                "reason": decision.reason,
            }

        # Save after EVERY batch.
        save_results(
            text_blocks,
            existing,
        )

        print(
            f"Saved {len(existing)} results"
        )

    return existing


def main():

    from app.ingestion.docling_parser import (
        parse_with_docling,
    )

    from app.ingestion.docling_structure import (
        extract_docling_structure,
    )

    document = parse_with_docling(
        "/home/ruproy9924/important/InsightFlow/uploads/attention_is_all_u_need.pdf"
    )

    blocks = extract_docling_structure(
        document
    )

    results = analyze_text_continuity(
        blocks
    )

    print()
    print("=" * 60)
    print("CONTINUITY ANALYSIS")
    print("=" * 60)

    print(
        f"Results: {len(results)}"
    )

    print(
        f"CONTINUE: "
        f"{sum(r['decision'] == 'CONTINUE' for r in results.values())}"
    )

    print(
        f"SEPARATE: "
        f"{sum(r['decision'] == 'SEPARATE' for r in results.values())}"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()