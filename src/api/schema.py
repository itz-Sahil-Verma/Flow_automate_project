from pydantic import BaseModel

class SearchResult(BaseModel):
    file_name: str
    page_number: int
    content_type: str 
    text: str
