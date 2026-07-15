import yaml
import json
from pathlib import Path

from models import Course, CourseState

def load_courses() -> list[Course]:
    courses = []
    with open("../data/courses.yml") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for name, info in data['courses'].items():
        courses.append(
            Course(
                name=name, 
                url=info["url"], 
                role_id=info["role_id"],
            )
        )

    return courses

def load_state() -> dict[str, CourseState]:
    if not Path("../data/state.json").exists():
        return {}

    with open("../data/state.json") as file:
        data = json.load(file)

    state = {}

    for name, info in data.items():
        state[name] = CourseState(latest_url= info["latest_url"])

    return state

def save_state(state: dict[str, CourseState]) -> None:
    data = {}

    for name, course_state in state.items():
        data[name] = {"latest_url": course_state.latest_url}

    with open("../data/state.json", "w") as file:
        json.dump(data, file, indent=4)
