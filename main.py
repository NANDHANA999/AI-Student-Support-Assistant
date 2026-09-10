"""AI Student Support Assistant.

This is a small, dependency-light reference implementation of the workflow
described in the internship report:

    query -> retrieve relevant resource -> return a concise response

Text resources are indexed automatically. Image resources can be processed
with the optional OCR command:

    python main.py --ocr path/to/examination_notice.png
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ocr_module import extract_text_from_image


SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md"}
SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "in",
    "is",
    "me",
    "of",
    "on",
    "please",
    "student",
    "tell",
    "the",
    "to",
    "what",
    "when",
    "where",
    "who",
}


def tokenize(value: str) -> set[str]:
    """Return useful lowercase words from a query or document."""
    words = re.findall(r"[a-z0-9]+", value.lower())
    return {word for word in words if word not in STOP_WORDS and len(word) > 1}


@dataclass(frozen=True)
class Resource:
    """A searchable resource loaded from disk."""

    name: str
    path: Path
    text: str

    @property
    def terms(self) -> set[str]:
        return tokenize(f"{self.name} {self.text}")


class StudentSupportAssistant:
    """Search student-support resources and answer terminal queries."""

    def __init__(self, resources_dir: Path = Path("resources")) -> None:
        self.resources_dir = resources_dir
        self.resources = self._load_resources()

    def _load_resources(self) -> list[Resource]:
        if not self.resources_dir.exists():
            return []

        loaded: list[Resource] = []
        for path in sorted(self.resources_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
                text = path.read_text(encoding="utf-8")
                if text.strip():
                    loaded.append(Resource(path.stem.replace("_", " "), path, text))
        return loaded

    def search(self, query: str, limit: int = 3) -> list[tuple[Resource, int]]:
        """Rank resources by query-term overlap."""
        query_terms = tokenize(query)
        if not query_terms:
            return []

        scored: list[tuple[Resource, int]] = []
        for resource in self.resources:
            score = len(query_terms & resource.terms)
            if score:
                scored.append((resource, score))
        return sorted(scored, key=lambda item: (-item[1], item[0].name))[:limit]

    def answer(self, query: str) -> str:
        matches = self.search(query)
        if not matches:
            return (
                "I could not find that information in the available resources. "
                "Try asking about the exam schedule, student guidelines, "
                "library hours, or contact details."
            )

        best_resource, best_score = matches[0]
        response = best_resource.text.strip()
        return (
            f"Relevant resource: {best_resource.name}\n"
            f"Match score: {best_score}\n\n"
            f"{response}"
        )

    def ocr(self, image_path: Path) -> str:
        """Extract text from an image and optionally save it as a resource."""
        text = extract_text_from_image(image_path)
        if not text.strip():
            return "OCR completed, but no text was detected."

        output_path = self.resources_dir / f"{image_path.stem}_ocr.txt"
        self.resources_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text.strip() + "\n", encoding="utf-8")
        self.resources = self._load_resources()
        return f"OCR text saved to {output_path}:\n\n{text.strip()}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Student Support Assistant")
    parser.add_argument(
        "--resources",
        type=Path,
        default=Path("resources"),
        help="directory containing .txt or .md student resources",
    )
    parser.add_argument("--query", help="answer one query and exit")
    parser.add_argument(
        "--ocr",
        type=Path,
        metavar="IMAGE",
        help="extract text from an image with Tesseract and save it as a resource",
    )
    return parser


def interactive_loop(assistant: StudentSupportAssistant) -> None:
    print("AI Student Support Assistant")
    print("Type a question, or type 'exit' to quit.")
    print(f"Loaded resources: {len(assistant.resources)}")

    while True:
        try:
            query = input("\nStudent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if query.lower() in {"exit", "quit"}:
            print("Goodbye.")
            return
        if not query:
            print("Please enter a question.")
            continue
        print(f"\nAssistant> {assistant.answer(query)}")


def main() -> None:
    args = build_parser().parse_args()
    assistant = StudentSupportAssistant(args.resources)

    if args.ocr:
        print(assistant.ocr(args.ocr))
        return
    if args.query:
        print(assistant.answer(args.query))
        return
    interactive_loop(assistant)


if __name__ == "__main__":
    main()