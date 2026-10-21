from fastapi import FastAPI

from routers import goals, students

app = FastAPI()

# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}

# Student endpoints
app.include_router(students.router)
# Goals endpoints
app.include_router(goals.router)