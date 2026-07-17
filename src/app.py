from fastapi import FastAPI
from checker import check_all_courses

app = FastAPI()

@app.get("/check-courses")
def check():
    check_all_courses()
    return {"status": "success"}