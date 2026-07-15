from dataclasses import dataclass

@dataclass
class Course:
    name: str
    url: str
    role_id: str


@dataclass
class Announcement:
    title: str
    url: str
    author: str
    date: str
    body: str


@dataclass
class CourseState:
    latest_url: str