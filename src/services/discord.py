import os
import requests

from models import Course, Announcement

# WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1527072899876524135/HvC-MTFfyzEv6xye8UmxRZtAsSEvu5DVkwsoZaWu4SmGBMiOXOAX8fJtu7GHMMbgKt-X"

def send_announcement(course: Course, announcement: Announcement) -> None:
    payload = {
        "content": f"Novo anúncio de {course.name} <@&{course.role_id}>!",

        "embeds": [
            {
                "title": announcement.title,
                "author": {
                    "name": announcement.author
                },
                "description": announcement.body,
                "url": announcement.url,
                "color": 0x0099ff,
                "footer": {
                    "text": f"{course.name} • {announcement.date}"
                }
            }
        ]
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(e)
