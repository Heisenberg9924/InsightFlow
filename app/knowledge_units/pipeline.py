from app.models.document import ParsedDocument

from app.knowledge_units.builder import KnowledgeUnitBuilder
from app.knowledge_units.section_builder import SectionBuilder
from app.knowledge_units.section_merger import SectionMerger
from app.knowledge_units.section_splitter import SectionSplitter


class KnowledgePipeline:

    def __init__(self):

        self.section_builder = SectionBuilder()
        self.section_merger = SectionMerger()
        self.section_splitter = SectionSplitter()

        self.builder = KnowledgeUnitBuilder()

    def build(self, document: ParsedDocument):

        sections = self.section_builder.build(document)

        sections = self.section_merger.merge(sections)

        sections = self.section_splitter.split(sections)

        return self.builder.build(sections)