from fastapi import FastAPI

from routers import students

app = FastAPI()

# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}

app.include_router(students.router)