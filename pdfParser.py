"""
PDF parser utilities: read PDFs (single/double column), write to text, parse all PDFs in a folder.
Requires: pip install pdfplumber
"""
from pathlib import Path
from tqdm import tqdm

import pdfplumber

BASE_FOLDER = "Literature_Review_Papers/"
OUTPUT_FILE_PUNNOOSE = "Literature_Review_Papers_Text/punnoose_papers.txt"
OUTPUT_FILE_DEEPA = "Literature_Review_Papers_Text/deepa_papers.txt"


def readPdf(path: str) -> str:
    """
    Read a PDF file from a path and return its text content.
    Handles both single-column and double-column (professional paper) layouts.

    Args:
        path: Path to the PDF file.

    Returns:
        Extracted text as a string. Returns empty string on error.
    """
    path = Path(path)
    if not path.exists() or path.suffix.lower() != ".pdf":
        return ""

    all_text = []

    try:
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_width = page.width
                page_height = page.height
                words = page.extract_words()

                # Detect multi-column (double-column) layout
                is_multi_column = False
                if words and len(words) >= 20:
                    midpoint = page_width / 2
                    left_words = sum(1 for w in words if (w["x0"] + w["x1"]) / 2 < midpoint)
                    right_words = sum(1 for w in words if (w["x0"] + w["x1"]) / 2 > midpoint)
                    total = len(words)
                    is_multi_column = (left_words / total >= 0.3 and right_words / total >= 0.3)

                if is_multi_column:
                    split_point = page_width * 0.5
                    left_text = page.crop((0, 0, split_point, page_height)).extract_text() or ""
                    right_text = page.crop((split_point, 0, page_width, page_height)).extract_text() or ""
                    page_text = f"{left_text}\n\n{right_text}".strip()
                else:
                    page_text = page.extract_text() or ""

                if page_text:
                    all_text.append(f"=== Page {page_num} ===\n{page_text}")

        return "\n\n".join(all_text)
    except Exception:
        return ""

def writeToTxt(path: str, content: str, title: str) -> None:
    """
    Write content to a text file. Creates the file if it does not exist.
    If the file already exists and has content, adds 2 newlines then appends.

    Args:
        path: Path to the text file.
        content: Text content to write.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    add_separator = path.exists() and path.stat().st_size > 0

    with open(path, "a", encoding="utf-8") as f:
        if add_separator:
            f.write(f"\n\nPaper:{title}\n")
        f.write(content)

def count_tokens(content: str) -> int:
    """
    Return an estimate of the number of tokens in the content.
    Uses ~4 characters per token (typical for English and common LLM tokenizers).
    For exact counts with a specific model, use that model's tokenizer (e.g. tiktoken).

    Args:
        content: Text to count tokens for.

    Returns:
        Estimated token count.
    """
    if not content or not content.strip():
        return 0
    return max(1, len(content.strip()) // 4)

def parseSubFiles(baseFolder: str) -> None:
    """
    Parse all PDF files under the base folder (recursively). For each PDF,
    reads content with readPdf and writes it to a .txt file with the same
    name in the same directory using writeToTxt.

    Args:
        baseFolder: Path to the root folder to scan for PDFs.
    """
    base = Path(baseFolder)
    punnooseTokens = 0
    deepaTokens = 0
    if not base.is_dir():
        return

    for pdf_path in tqdm(base.rglob("*.pdf"), desc="Parsing PDFs..."):
        fileName = pdf_path.name
        folderName = str(pdf_path.parent.name)
        content = readPdf(str(pdf_path))
        txt_path = pdf_path.with_suffix(".txt")
        if '+' in folderName:
            tokenCount = count_tokens(content)
            punnooseTokens += tokenCount
            writeToTxt(OUTPUT_FILE_PUNNOOSE, content, fileName)
        else:
            tokenCount = count_tokens(content)
            deepaTokens += tokenCount
            writeToTxt(OUTPUT_FILE_DEEPA, content, fileName)

    print(f"Total tokens for files by Deepa: {deepaTokens}")
    print(f"Total tokens for files by Punnoose: {punnooseTokens}")

parseSubFiles(BASE_FOLDER)
