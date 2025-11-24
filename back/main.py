from fastapi import FastAPI

app = FastAPI(title="API Ptut")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/books")
async def get_books():
    return [{"id": 1, "title": "Book 1"}, {"id": 2, "title": "Book 2"}]
