from storage import load_courses, load_state, save_state
from models import Course, CourseState
from services.fenix import get_latest_announcement
from services.discord import send_announcement

from fastapi import FastAPI

app = FastAPI()

@app.get("/check-courses")
def check_courses():
    print("Starting Announcement Checker...")
    courses = load_courses()
    state = load_state()

    for course in courses:
        print(f"Checking {course.name}")
        announcement = get_latest_announcement(course)

        if announcement is None:
            continue

        if(course.name not in state or announcement.url != state[course.name].latest_url):
            send_announcement(course, announcement)

            state[course.name] = CourseState(latest_url=announcement.url)

    save_state(state)

    print("Finished!!\n")

    return {"status": "success"}