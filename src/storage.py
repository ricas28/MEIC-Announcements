import os
import yaml
from pathlib import Path

from models import Course

from upstash_redis import Redis

from dotenv import load_dotenv

load_dotenv()

redis = Redis.from_env()

# Gets the path for main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Goes up to root
PROJECT_ROOT = os.path.dirname(BASE_DIR)

YAML_PATH = os.path.join(PROJECT_ROOT, "data/courses.yml")

def load_courses() -> list[Course]:
    courses = []

    with open(YAML_PATH, encoding="utf-8") as stream:
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

def get_latest_state(course_name: str) -> str | None:
    return redis.get(course_name)

def set_state(course_name: str, url: str) -> None:
    redis.set(course_name, url)
    