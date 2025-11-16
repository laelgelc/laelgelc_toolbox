# tests/pdf_scrape/test_core.py

from __future__ import annotations

from pathlib import Path

import pytest

from cl.pdf_scrape.core import (
    PdfToTextResult,
    extract_text_from_pdf,
    find_pdfs_in_path,
    pdfs_to_text,
)

# Helper: path to directory containing this test file
HERE = Path(__file__).parent
DATA_DIR = HERE / "data"


@pytest.mark.skipif(
    not (DATA_DIR / "sample.pdf").exists(),
    reason="sample.pdf test fixture is missing",
)
def test_extract_text_from_pdf_basic() -> None:
    pdf_path = DATA_DIR / "sample.pdf"
    text = extract_text_from_pdf(pdf_path)

    assert isinstance(text, str)
    assert text  # not empty (depends on fixture content)


def test_find_pdfs_in_path_file(tmp_path: Path) -> None:
    pdf_file = tmp_path / "doc.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\n%EOF\n")  # minimal fake PDF header

    result = find_pdfs_in_path(pdf_file)
    assert result == [pdf_file]


def test_find_pdfs_in_path_directory(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4\n%EOF\n")
    (tmp_path / "b.PDF").write_bytes(b"%PDF-1.4\n%EOF\n")
    (tmp_path / "c.txt").write_text("not a pdf")

    pdfs = find_pdfs_in_path(tmp_path)
    assert len(pdfs) == 2
    assert all(p.suffix.lower() == ".pdf" for p in pdfs)


def test_pdfs_to_text_creates_txt_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Create two fake PDFs
    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"
    pdf1.write_bytes(b"%PDF-1.4\n%EOF\n")
    pdf2.write_bytes(b"%PDF-1.4\n%EOF\n")

    # Monkeypatch extract_text_from_pdf to avoid needing real PDFs
    def fake_extract(pdf_path: Path) -> str:
        return f"Content of {pdf_path.name}"

    monkeypatch.setattr(
        "cl.pdf_scrape.core.extract_text_from_pdf",
        fake_extract,
    )

    results = pdfs_to_text(input_path=tmp_path, output_dir=None, overwrite=True)

    assert len(results) == 2
    for r in results:
        assert r.status == "created"
        assert r.txt_path.is_file()
        assert r.txt_path.read_text(encoding="utf-8").startswith("Content of ")


def test_pdfs_to_text_skips_existing_when_overwrite_false(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pdf = tmp_path / "doc.pdf"
    pdf.write_bytes(b"%PDF-1.4\n%EOF\n")
    txt = tmp_path / "doc.txt"
    txt.write_text("existing", encoding="utf-8")

    def fake_extract(pdf_path: Path) -> str:
        return "new content"

    monkeypatch.setattr(
        "cl.pdf_scrape.core.extract_text_from_pdf",
        fake_extract,
    )

    results = pdfs_to_text(input_path=pdf, output_dir=None, overwrite=False)
    assert len(results) == 1

    result = results[0]
    assert result.status == "skipped"
    assert result.txt_path == txt
    assert txt.read_text(encoding="utf-8") == "existing"