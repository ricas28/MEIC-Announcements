# MEIC Announcements

A lightweight service that monitors Fénix course announcement pages and sends new announcements to a Discord server using a webhook.

The application periodically checks the latest announcement for each configured course and only sends a notification if a new announcement is detected.

## Features

- Monitor multiple Fénix course pages
- Discord webhook notifications
- Markdown formatting for announcement bodies
- Stores the latest announcement state in Redis
- Easy to deploy to any Python hosting platform

---

## Project Structure

```
.
├── src/
│   ├── app.py          # FastAPI
│   ├── main.py         # Run locally
│   ├── checker.py      # Main logic for checking courses
│   ├── models.py
│   ├── storage.py
│   ├── requirements.txt
│   └── services/
│       ├── discord.py
│       └── fenix.py
│ 
├── data/
│   └── courses.yml
│ 
├── .env.sample
└── README.md
```

---

## Requirements

- Python 3.12+
- Redis database
- Discord webhook

---

## Installation

Clone the repository

```bash
git clone https://github.com/ricas28/MEIC-Announcements.git
cd MEIC-Announcements
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install the dependencies

```bash
pip install -r src/requirements.txt
```

---

## Environment Variables

A sample environment file is included in the repository.

Copy it to a new `.env` file:

```bash
cp .env.sample .env
```

On Windows (PowerShell):

```powershell
Copy-Item .env.sample .env
```

Then edit `.env` and fill in your own values:

```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
UPSTASH_REDIS_REST_URL=//...
UPSTASH_REDIS_REST_TOKEN=//...
```

---

## Configuring Courses

Courses are configured in `data/courses.yml`.

Example:

```yaml
- Sistemas Operativos:
    url: https://fenix.tecnico.ulisboa.pt/...
    role_id: 123456789012345678

- Inteligência Artificial:
    url: https://fenix.tecnico.ulisboa.pt/...
    role_id: 987654321098765432
```

Each course contains:

- `name` – displayed in Discord
- `url` – Fénix announcements page
- `role_id` – Discord role to mention

---

## Running Locally

### Run a Single Scan

Execute the application once from the command line:

```bash
python src/main.py
```

### Run the API

Start the FastAPI server:

```bash
python -m uvicorn src.app:app --reload 
```

The API will be available at:

```
http://localhost:8000
```

To manually trigger a scan:

```bash
curl http://localhost:8000/check-courses
```

---

## Example Deployment

This project also exposes an HTTP endpoint (`/check-courses`) that performs a single scan.

To run it periodically, deploy the application to a hosting provider and configure an external scheduler to send requests to the endpoint.

My deployment uses:

- **Render** – hosts the FastAPI application
- **Upstash Redis** – stores the latest announcement URL for each course
- **cron-job.org** – sends a `GET /check-courses` request every 5 minutes
- **Discord Webhook** – delivers notifications

This architecture avoids running a permanent background process while keeping the service lightweight and inexpensive.

---

## How It Works

Every execution:

1. Load all configured courses.
2. Download the course announcements page.
3. Extract the latest announcement.
4. Compare its URL with the value stored in Redis.
5. If different:
   - Send a Discord notification.
   - Update Redis.
6. Continue with the next course.

Since only the latest announcement URL is stored, the database remains extremely small regardless of how many announcements have been published.

---

## Technologies

- Python
- BeautifulSoup
- Requests
- Markdownify
- Redis
- Discord Webhooks

---

## License

MIT