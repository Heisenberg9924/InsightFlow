from app.parsers.pdf_parser import extract_pdf_text
from app.parsers.docx_parser import extract_docx_text
from app.parsers.txt_parser import extract_txt_text
from app.parsers.markdown_parser import extract_markdown_text
from app.parsers.csv_parser import extract_csv_text
from app.parsers.excel_parser import extract_excel_text
from app.models.document import ParsedDocument


def parse_document(file_path: str) -> ParsedDocument:

    path = file_path.lower()

    if path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif path.endswith(".docx"):
        return extract_docx_text(file_path)

    elif path.endswith(".txt"):
        return extract_txt_text(file_path)

    elif path.endswith(".md"):
        return extract_markdown_text(file_path)

    elif path.endswith(".csv"):
        return extract_csv_text(file_path)

    elif path.endswith(".xlsx"):
        return extract_excel_text(file_path)

    raise ValueError("Unsupported file format")