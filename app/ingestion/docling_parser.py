from pathlib import Path

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    RapidOcrOptions,
)


pipeline_options = PdfPipelineOptions(
    do_ocr=True,
)

pipeline_options.ocr_options = RapidOcrOptions(
    lang=["en"],
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)


def parse_with_docling(path: str):
    source = Path(path)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    result = converter.convert(source)

    return result.document