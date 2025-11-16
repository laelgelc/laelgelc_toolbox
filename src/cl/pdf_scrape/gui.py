# src/cl/pdf_scrape/gui.py

from __future__ import annotations

from pathlib import Path
from typing import List

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from cl.pdf_scrape.core import PdfToTextResult, pdfs_to_text


class PdfScraperApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PDF Scraper - Phase 1")
        self.geometry("600x400")

        self._build_widgets()

    def _build_widgets(self) -> None:
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=10)

        select_btn = tk.Button(
            frame,
            text="Select PDF file(s)...",
            command=self.select_files,
        )
        select_btn.pack(side=tk.LEFT)

        dir_btn = tk.Button(
            frame,
            text="Select folder...",
            command=self.select_folder,
        )
        dir_btn.pack(side=tk.LEFT, padx=(10, 0))

        self.overwrite_var = tk.BooleanVar(value=False)
        overwrite_check = tk.Checkbutton(
            frame,
            text="Overwrite existing .txt",
            variable=self.overwrite_var,
        )
        overwrite_check.pack(side=tk.LEFT, padx=(20, 0))

        self.log = scrolledtext.ScrolledText(self, state="disabled", height=18)
        self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def log_message(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")
        self.update_idletasks()

    def run_scrape(self, input_path: Path) -> None:
        try:
            results: List[PdfToTextResult] = pdfs_to_text(
                input_path=input_path,
                output_dir=None,
                overwrite=self.overwrite_var.get(),
            )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.log_message(f"Error: {exc}")
            return

        created = sum(1 for r in results if r.status == "created")
        skipped = sum(1 for r in results if r.status == "skipped")
        errors = [r for r in results if r.status == "error"]

        self.log_message(f"Processed {len(results)} file(s).")
        self.log_message(f"  created: {created}")
        self.log_message(f"  skipped (existing .txt): {skipped}")
        self.log_message(f"  errors: {len(errors)}")

        for r in results:
            if r.status == "created":
                self.log_message(f"[created] {r.pdf_path} -> {r.txt_path}")
            elif r.status == "skipped":
                self.log_message(
                    f"[skipped] {r.pdf_path} (existing {r.txt_path})"
                )
            elif r.status == "error":
                self.log_message(
                    f"[error]   {r.pdf_path} -> {r.txt_path} : {r.error}"
                )

        if errors:
            messagebox.showwarning(
                "Done with errors",
                f"Processed {len(results)} PDF file(s) with "
                f"{len(errors)} error(s). See log for details.",
            )
        else:
            messagebox.showinfo(
                "Done",
                f"Processed {len(results)} PDF file(s).",
            )

    def select_files(self) -> None:
        filenames = filedialog.askopenfilenames(
            title="Select PDF file(s)",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not filenames:
            return

        for name in filenames:
            self.run_scrape(Path(name))

    def select_folder(self) -> None:
        directory = filedialog.askdirectory(title="Select folder containing PDFs")
        if not directory:
            return
        self.run_scrape(Path(directory))


def run_gui() -> None:
    app = PdfScraperApp()
    app.mainloop()


if __name__ == "__main__":
    run_gui()