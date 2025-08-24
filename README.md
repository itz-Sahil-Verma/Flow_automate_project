# PDF ETL & Search Project

This project is designed to extract, transform, and search content from PDF files using **FastAPI** and **Elasticsearch/OpenSearch**. It provides a secure search API for querying structured content (text, tables, images) from PDFs.

---

## Project Structure

├── data
│ └── parsed_pdf
│ └── flow_automate_pitch_parsed.json # Example parsed PDF content
├── requirements.txt # Python dependencies
├── run_etl.py # ETL pipeline runner
├── src
│ ├── api # FastAPI application
│ │ ├── main.py # FastAPI main entry point
│ │ └── routes.py # API route definitions
│ └── etl # ETL modules
│ ├── 1_extract_data.py # PDF extraction logic
│ ├── 2_transform.py # Transform extracted content
│ └── 3_load.py # Load transformed data to Elasticsearch
└── venv # Virtual environment


---

## ETL Pipeline

The ETL pipeline orchestrates the extraction, transformation, and loading of PDF data into Elasticsearch.

### 1. Extract (`1_extract_data.py`)
- Calls a PDF parser with a PDF file.
- Returns structured JSON content including text, tables, images, and metadata.

### 2. Transform (`2_transform.py`)
- Cleans text using Python’s `re` module.
- Splits text into sentences using **NLTK**.
- Processes images via **OCR (Tesseract)** to extract text.
- Serializes table data into descriptive lines.
- Consolidates all transformed content into a single variable `doc`.

### 3. Load (`3_load.py`)
- Performs **bulk upload** of transformed documents into Elasticsearch/OpenSearch.
- Each document includes:
  - `file_name`
  - `page_number`
  - `content_type`
  - `text`
  - `metadata`

---

## API Folder (`src/api`)

- Built using **FastAPI**.
- **Main file (`main.py`)** initializes the FastAPI app.
- **Routes file (`routes.py`)** defines the API endpoints.

### `/search` API
- Accepts a **query** and an **API key**.
- **API Key Security**: Requests without a valid key return **403 Unauthorized**.
- Sends valid queries to Elasticsearch/OpenSearch.
- Returns documents containing the search term with:
  - `file_name`
  - `page_number`
  - `content_type`
  - `text`

---

## Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
