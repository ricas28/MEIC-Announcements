from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md

from models import Course, Announcement

def get_announcement_content(url: str) -> requests.Response:
    "Makes a GET request to retrieve html page for course announcement."
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    return response

def get_latest_announcement(course: Course) -> Announcement:
    """Returns the latest announcement from the given course"""

    try:
        html_content = get_announcement_content(course.url)

    except requests.RequestException as e:
        print(f"Failed to fetch {course.name}: {e}")
        return None

    soup = BeautifulSoup(html_content.content, 'html.parser')

    # Get div for announcements.
    announcement_div = soup.find("div", class_="col-sm-9 main-content", id="content-block")

    if not announcement_div:
        return None

    # First match is the latest announcement
    latest_announcement = announcement_div.find("div")

    if not latest_announcement:
        return None

    # Titles are always written with 'h5' tag, followed by an 'a' tag
    title_tag = latest_announcement.find("h5").find("a")

    # Paragraph for author and date
    first_p = latest_announcement.find("p")

    spans = first_p.find_all("span")

    date = spans[0].text

    author = spans[-1].text

    title = title_tag.text
    url = title_tag.get("href")

    # Erase title
    title_tag.parent.decompose() 
    # Erase author paragraph
    first_p.decompose()

    body = md(str(latest_announcement))

    return Announcement(title=title, url=url, author=author, date=date, body=body)