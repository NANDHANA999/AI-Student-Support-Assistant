"""Optional OCR support using Tesseract and Pillow."""

from pathlib import Path


def extract_text_from_image(image_path: Path) -> str:
    """Extract text from an image.

    OCR dependencies are optional so the text-search assistant still works
    when Tesseract is not installed.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        import pytesseract
        from PIL import Image
    except ImportError as error:
        raise RuntimeError(
            "OCR dependencies are missing. Run: pip install -r requirements.txt"
        ) from error

    try:
        return pytesseract.image_to_string(Image.open(image_path))
    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError(
            "Tesseract OCR is not installed or is not on PATH. "
            "Install Tesseract, then run this command again."
        ) from error