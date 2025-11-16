# src/cl/pdf_scrape/core.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import fitz  # PyMuPDF


@dataclass
class PdfToTextResult:
    """Result of converting a single PDF to text."""
    pdf_path: Path
    txt_path: Path
    status: str  # "created", "skipped", "error"
    error: Optional[Exception] = None


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract all text from a single PDF file using PyMuPDF.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a PDF.
        fitz.FitzError: On PDF parsing errors.
    """
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")

    text_parts: List[str] = []

    # fitz.open accepts a path-like object
    with fitz.open(pdf_path) as doc:
        for page in doc:
            # "text" -> layout-ish text; you can tweak to "blocks" or "dict" later
            text_parts.append(page.get_text("text"))

    return "\n".join(text_parts)


def find_pdfs_in_path(path: Path) -> List[Path]:
    """
    Return a list of PDF files for a given path.

    If `path` is a file:
        - Return [path] if it's a PDF, otherwise raise ValueError.
    If `path` is a directory:
        - Return all direct children ending with .pdf (non-recursive).
    """
    if path.is_file():
        if path.suffix.lower() == ".pdf":
            return [path]
        raise ValueError(f"File is not a PDF: {path}")

    if path.is_dir():
        return sorted(
            p for p in path.iterdir()
            if p.is_file() and p.suffix.lower() == ".pdf"
        )

    raise FileNotFoundError(f"Path not found: {path}")


def pdfs_to_text(
        input_path: Path,
        output_dir: Path | None = None,
        overwrite: bool = False,
        encoding: str = "utf-8",
) -> List[PdfToTextResult]:
    """
    Convert one or more PDFs to .txt files.

    Args:
        input_path:
            A single PDF file or a directory containing PDFs.
        output_dir:
            If provided, all .txt files are written there (mirroring PDF base names).
            If None, each .txt is written alongside its PDF.
        overwrite:
            If True, existing .txt files are overwritten.
            If False, existing .txt files are left as-is and marked as "skipped".
        encoding:
            Encoding to use when writing text files (default: utf-8).

    Returns:
        A list of PdfToTextResult objects, one per PDF.

    Raises:
        FileNotFoundError:
            If input_path doesn't exist, or (for a directory) no PDFs are found.
        ValueError:
            If input_path is a non-PDF file.
    """
    input_path = input_path.expanduser().resolve()
    pdfs = find_pdfs_in_path(input_path)

    if not pdfs:
        # This only happens when input_path is a directory
        raise FileNotFoundError(f"No PDF files found in: {input_path}")

    results: List[PdfToTextResult] = []

    if output_dir is not None:
        output_dir = output_dir.expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdfs:
        if output_dir is None:
            txt_path = pdf_path.with_suffix(".txt")
        else:
            txt_path = output_dir / (pdf_path.stem + ".txt")

        # Default assumption: we'll succeed
        status = "created"
        error: Optional[Exception] = None

        if txt_path.exists() and not overwrite:
            status = "skipped"
        else:
            try:
                text = extract_text_from_pdf(pdf_path)
                txt_path.write_text(text, encoding=encoding)
            except Exception as exc:  # pragma: no cover (you can narrow this later)
                status = "error"
                error = exc

        results.append(
            PdfToTextResult(
                pdf_path=pdf_path,
                txt_path=txt_path,
                status=status,
                error=error,
            )
        )

    return results