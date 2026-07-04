from app.knowledge_units.section_builder import Section


class SectionSplitter:

    def __init__(self, max_words: int = 500):
        self.max_words = max_words

    def _word_count(self, text: str) -> int:
        return len(text.split())

    def split(self, sections: list[Section]) -> list[Section]:

        output = []

        for section in sections:

            if self._word_count(section.content) <= self.max_words:
                output.append(section)
                continue

            paragraphs = section.content.split("\n\n")

            current = []
            current_words = 0

            for paragraph in paragraphs:

                words = self._word_count(paragraph)

                if current_words + words > self.max_words:

                    output.append(
                        Section(
                            title=section.title,
                            content="\n\n".join(current),
                        )
                    )

                    current = [paragraph]
                    current_words = words

                else:

                    current.append(paragraph)
                    current_words += words

            if current:

                output.append(
                    Section(
                        title=section.title,
                        content="\n\n".join(current),
                    )
                )

        return output