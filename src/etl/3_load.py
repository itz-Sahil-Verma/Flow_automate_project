from elasticsearch import helpers, Elasticsearch
import datetime
import os
from logger import get_logger

logger = get_logger(__name__)

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "pdf_documents")

def load_to_elasticsearch_bulk(docs, index_name=ELASTICSEARCH_INDEX):
    """Loads a list of documents into Elasticsearch using bulk helper."""
    es = Elasticsearch(ELASTICSEARCH_HOST)
    logger.info("Starting bulk insert of %d documents into index: %s", len(docs), index_name)

    actions = [
        {
            "_index": index_name,
            "_source": {
                "file_name": doc.get("file_name"),
                "page_number": doc.get("page_number"),
                "content_type": doc.get("content_type"),
                "text": doc.get("text"),
                "metadata": {
                    **doc.get("metadata", {}),
                    "ingested_at": datetime.datetime.utcnow().isoformat()
                }
            }
        }
        for doc in docs
    ]

    try:
        success_count, errors = helpers.bulk(es, actions, raise_on_error=False)
        logger.info("Successfully indexed %d documents.", success_count)
        if errors:
            logger.warning("Failed to index %d documents.", len(errors))
    except Exception as e:
        logger.error("Error during bulk insert: %s", e)
        raise
