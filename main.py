from fastapi import FastAPI

app = FastAPI()

# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}