from pathlib import Path
from llama_cloud import LlamaCloud

from dotenv import load_dotenv

load_dotenv()

client = LlamaCloud()

def parse_documents(path: str) -> str:
    
    print("uploading....\n")
    
    file = client.files.create(  #upload
        file = Path(path),
        purpose = "parse",
    )
    
    print("uploaded\n")
    print("parsing....\n")    
    result = client.parsing.parse(
        file_id = file.id,
        tier = "agentic",
        version = "latest",
        expand = ["markdown"],
    )
    
    print("parsed")
    
    if result.markdown is None:
     raise RuntimeError("Markdown not available")

    pages = []

    for page in result.markdown.pages:
     if hasattr(page, "markdown"):
        pages.append(page.markdown)

    markdown = "\n\n".join(pages)

    return markdown