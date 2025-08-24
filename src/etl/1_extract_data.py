import json
from logger import get_logger

# this is our pdf extraction function, as of now there is no module we just use a dummay name
from pdf_parser import PDFParser  

logger = get_logger(__name__)

def extract(pdf_path: str) -> dict:

    logger.info("Starting extraction for file: %s", pdf_path)

    try:
        parser = PDFParser(pdf_path)
        parsed_response = parser.parse()
        logger.info("Extraction completed successfully for file: %s", pdf_path)
        return parsed_response

    except Exception as e:
        logger.error("Extraction failed for file %s: %s", pdf_path, e)
        raise
