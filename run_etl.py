import logging
from src import extract_from_pdf, transform, load_to_elasticsearch_bulk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def run_etl(file_path, index_name="pdf_documents"):
    logger.info("Starting ETL Pipeline...")

    # 1. Extract
    raw_docs = extract_from_pdf(file_path)
    logger.info(f"Extracted {len(raw_docs)} raw docs")

    # 2. Transform
    transformed = transform(raw_docs)
    logger.info(f"Transformed into {len(transformed)} docs")

    # 3. Load
    load_to_elasticsearch_bulk(transformed, index_name=index_name)
    logger.info("ETL Pipeline finished.")
