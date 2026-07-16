from storage import load_courses, set_state, get_latest_state
from models import Course
from services.fenix import get_latest_announcement
from services.discord import send_announcement

from fastapi import FastAPI

app = FastAPI()

@app.get("/check-courses")
def check_courses():
    print("Starting Announcement Checker...")
    courses = load_courses()

    for course in courses:
        print(f"Checking {course.name}")
        announcement = get_latest_announcement(course)

        state = get_latest_state(course.name)

        print(announcement)
        print(state)

        if announcement is None:
            continue

        if(announcement.url != state):
            send_announcement(course, announcement)

            set_state(course.name, announcement.url)


    print("Finished!!\n")

    return {"status": "success"}