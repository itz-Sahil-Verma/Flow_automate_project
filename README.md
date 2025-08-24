# Flow Automate Project

## Project Structure

```text
├── data
│   └── parsed_json
│       └── flow_automate_pitch_parsed.json
├── README.md
├── requirements.txt
├── run_etl.py
├── src
│   ├── api
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── schema.py
│   ├── etl
│   │   ├── __init__.py
│   │   ├── 1_extract_data.py
│   │   ├── 2_transform.py
│   │   └── 3_load.py
│   └── logger.py
```


### **Data Folder**
In the `data` folder, there is a parsed PDF named `flow_automate_pitch_parsed.json`. This file represents the expected output format returned by the PDF parser.

### **SRC Folder**
The `src` folder contains two subfolders: `api` and `etl`.

#### **ETL Subfolder**
This folder contains three main files:

1. **`1_extract_data.py`**  
   - Calls the PDF parser.
   - Sends a PDF file and expects a parsed response in the same structure as `flow_automate_pitch_parsed.json`.

2. **`2_transform.py`**  
   - Cleans the text using Python's `re` module.
   - Splits text into smaller sentences using the `nltk` library.
   - Converts images to text using OCR (`pytesseract`), then cleans and splits sentences.
   - Serializes tables into line format.
   - Stores all transformed data in a variable called `doc`.

3. **`3_load.py`**  
   - Bulk uploads all transformed documents to Elasticsearch.

The ETL pipeline is orchestrated in `run_etl.py`.

#### **API Subfolder**
The API is developed using the FastAPI framework:

- **`main.py`**  
  The FastAPI main application file.

- **`routes.py`**  
  - Contains the `/search` API.
  - Secured with an API key verified through the `get_api_key` function.
  - If the request is valid, the user-provided query is sent to Elasticsearch.
  - Returns the words or phrases where the query is found in the PDF documents.

---

