from llama_index.core import Document
from llama_index.core.node_parser import MarkdownNodeParser

node_parser = MarkdownNodeParser()

def create_nodes(markdown: str):
    document = Document(text = markdown)
    return node_parser.get_nodes_from_documents([document])