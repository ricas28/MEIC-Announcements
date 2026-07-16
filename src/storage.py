import yaml
import json
import os
from pathlib import Path

from models import Course, CourseState

# Gets the path for main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Goes up to root
PROJECT_ROOT = os.path.dirname(BASE_DIR)

YAML_PATH = os.path.join(PROJECT_ROOT, "data/courses.yml")

JSON_PATH = os.path.join(PROJECT_ROOT, "data/state.json")

def load_courses() -> list[Course]:
    courses = []
    with open("YAML_PATH", encoding="utf-8") as stream:
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
    if not Path("JSON_PATH").exists():
        return {}

    with open("JSON_PATH", encoding="utf-8") as file:
        data = json.load(file)

    state = {}

    for name, info in data.items():
        state[name] = CourseState(latest_url= info["latest_url"])

    return state

def save_state(state: dict[str, CourseState]) -> None:
    data = {}

    for name, course_state in state.items():
        data[name] = {"latest_url": course_state.latest_url}

    with open("JSON_PATH", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
