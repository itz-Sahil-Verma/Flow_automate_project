import re
import nltk
import pytesseract
from PIL import Image
from logger import get_logger

nltk.download("punkt", quiet=True)
logger = get_logger(__name__)

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remove non-alphanumeric (except punctuation), collapse spaces
    text = re.sub(r"[^a-zA-Z0-9\s.,!?;:()-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def split_sentences(text: str) -> list[str]:
    return nltk.sent_tokenize(text)

def transform_images(images: list[dict]) -> list[str]:
    """Convert images to text using OCR, then clean and split into sentences."""
    ocr_image_texts = []
    for img in images:
        try:
            text = pytesseract.image_to_string(Image.open(img["path"]))
            cleaned = clean_text(text)
            sentences = split_sentences(cleaned)
            ocr_image_texts.extend(sentences)
            logger.info("OCR processed image: %s, extracted %d sentences", img.get("path"), len(sentences))
        except Exception as e:
            logger.error("Error OCR processing image %s: %s", img.get("path"), e)
    return ocr_image_texts

def transform_tables(tables: list[dict]) -> list[str]:
    """Serialize tables into descriptive key-value pair lines."""
    table_lines = []
    for table_block in tables:
        table_data = table_block.get("data", [])
        if len(table_data) < 2:
            continue
        header = table_data[0]
        data_rows = table_data[1:]
        for row in data_rows:
            key_value_pairs = [f"{header[i]}: {cell}" for i, cell in enumerate(row)]
            line = ", ".join(key_value_pairs)
            table_lines.append(f"Table Row: {line}")
        logger.info("Processed table with %d rows", len(data_rows))
    return table_lines

def transform(parsed_response: dict) -> list:
    documents = []
    file_name = parsed_response.get("file_name", "unknown.pdf")
    logger.info("Starting transformation for file: %s", file_name)

    for page in parsed_response.get("pages", []):
        page_number = page.get("page_number")
        # Process text
        raw_text = page.get("text", "")
        cleaned_text = clean_text(raw_text)
        sentences = split_sentences(cleaned_text)
        logger.info("Page %d: extracted %d text sentences", page_number, len(sentences))

        # Process images
        images = page.get("images", [])
        ocr_sentences = transform_images(images)

        # Process tables
        tables = page.get("tables", [])
        serialized_tables = transform_tables(tables)

        all_sentences = sentences + ocr_sentences + serialized_tables

        documents.append({
            "file_name": file_name,
            "page_number": page_number,
            "content_type": "pdf_page",
            "text": " ".join(all_sentences),
            "metadata": {
                **page.get("metadata", {}),
                "num_sentences": len(all_sentences)
            }
        })
        logger.info("Page %d transformation complete, total sentences: %d", page_number, len(all_sentences))

    logger.info("Transformation completed for file: %s, total pages: %d", file_name, len(parsed_response.get("pages", [])))
    return documents
