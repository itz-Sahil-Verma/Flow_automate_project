from fastapi import FastAPI
from routes import search 

app = FastAPI(title="PDF Search API")

# Search API Router
app.include_router(search.router)

@app.get("/")
def home():
    return {"message": "Welcome to PDF Search API"}