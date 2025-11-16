# src/cl/pdf_scrape/cli.py

from __future__ import annotations

from pathlib import Path

import click

from .core import PdfToTextResult, pdfs_to_text
from . import gui as gui_module


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Directory to write .txt files to (default: alongside PDFs).",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing .txt files if they already exist.",
)
@click.option(
    "--gui",
    is_flag=True,
    default=False,
    help="Launch GUI instead of running in CLI mode.",
)
def main(
        input_path: Path,
        output_dir: Path | None,
        overwrite: bool,
        gui: bool,
) -> None:
    """
    Scrape text from PDF files and write .txt files.

    INPUT_PATH can be a single PDF file or a directory containing PDFs.
    """
    if gui:
        gui_module.run_gui()
        return

    try:
        results = pdfs_to_text(
            input_path=input_path,
            output_dir=output_dir,
            overwrite=overwrite,
        )
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)

    created = sum(1 for r in results if r.status == "created")
    skipped = sum(1 for r in results if r.status == "skipped")
    errors = [r for r in results if r.status == "error"]

    click.echo(f"Processed {len(results)} PDF file(s).")
    click.echo(f"  created: {created}")
    click.echo(f"  skipped (existing .txt): {skipped}")
    click.echo(f"  errors: {len(errors)}")

    for r in results:
        if r.status == "created":
            click.echo(f"[created] {r.pdf_path} -> {r.txt_path}")
        elif r.status == "skipped":
            click.echo(f"[skipped] {r.pdf_path} (existing {r.txt_path})")
        elif r.status == "error":
            click.echo(
                f"[error]   {r.pdf_path} -> {r.txt_path} : {r.error}",
                err=True,
            )


if __name__ == "__main__":
    main()