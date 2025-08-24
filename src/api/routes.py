from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import APIKeyHeader
from elasticsearch import Elasticsearch
from typing import List
from dotenv import load_dotenv
import os
from api.schema import SearchResult
from logger import get_logger 

load_dotenv()

API_KEY = os.getenv("API_KEY")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")

logger = get_logger(__name__)

es = Elasticsearch(ELASTICSEARCH_HOST)

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        logger.warning("Unauthorized API key attempt: %s", api_key)
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key


# Search API Endpoint
@app.get("/search", response_model=List[SearchResult])
def search_pdfs(query: str = Query(..., min_length=2), api_key: str = Depends(get_api_key)):
    logger.info("Received search query: '%s'", query)

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text", "file_name", "metadata.author", "metadata.title"]
            }
        }
    }

    try:
        resp = es.search(index=ELASTICSEARCH_INDEX, body=body, size=1000)
        hits = resp.get("hits", {}).get("hits", [])
        logger.info("Search returned %d hits for query: '%s'", len(hits), query)

    except Exception as e:
        logger.error("Elasticsearch search failed: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    results = [
        SearchResult(
            file_name=hit["_source"]["file_name"],
            page_number=hit["_source"]["page_number"],
            content_type=hit["_source"]["content_type"],
            text=hit["_source"]["text"],
        )
        for hit in hits
    ]

    return results
