from app.knowledge_units.section_builder import Section


class SectionMerger:

    def __init__(
        self,
        min_words: int = 75,
        max_words: int = 600,
    ):
        self.min_words = min_words
        self.max_words = max_words

    def _word_count(self, text: str) -> int:
        return len(text.split())

    def merge(self, sections: list[Section]) -> list[Section]:

        if not sections:
            return []

        merged = [sections[0]]

        for current in sections[1:]:

            previous = merged[-1]

            previous_words = self._word_count(previous.content)
            current_words = self._word_count(current.content)

            # Merge only if:
            # 1. Current section is small.
            # 2. Merging won't exceed max size.
            if (
                current_words < self.min_words
                and previous_words + current_words <= self.max_words
            ):

                previous.content += (
                    f"\n\n{current.title}\n"
                    f"{current.content}"
                )

            else:

                merged.append(current)

        return merged