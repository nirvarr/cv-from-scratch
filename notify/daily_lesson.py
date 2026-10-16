import os
import sys
import json
import argparse
import urllib.request
import datetime
from zoneinfo import ZoneInfo

def select_lesson(start_date_str, timezone_str, num_lessons, override_day=None, current_date=None):
    """
    Computes which lesson to show based on the start date and timezone.
    Pure function for easy testing.
    """
    if override_day is not None:
        # 1-based day, wrap it around
        index = (override_day - 1) % num_lessons
        return index

    tz = ZoneInfo(timezone_str)

    if current_date is None:
        current_date = datetime.datetime.now(tz).date()

    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()

    days_since = (current_date - start_date).days

    if days_since < 0:
        index = 0
    else:
        index = days_since % num_lessons

    return index

def build_message(lesson_data, site_url):
    """
    Builds the message payload.
    """
    day = lesson_data["day"]
    title = lesson_data["title"]
    summary = lesson_data["summary"]

    # Ensure site_url ends with slash if it doesn't already have query params
    base_url = site_url.rstrip("/") + "/"
    click_url = f"{base_url}?day={day}"

    return {
        "title": f"Day {day}: {title}",
        "message": f"{title}\n\n{summary}",
        "click": click_url
    }

def main():
    parser = argparse.ArgumentParser(description="Send daily lesson notification via ntfy.sh")
    parser.add_argument("--dry-run", action="store_true", help="Print the message instead of sending")
    parser.add_argument("--day", type=int, help="Override the current day (1-based index)")
    args = parser.parse_args()

    with open("lessons.json", "r") as f:
        data = json.load(f)

    start_date = data["start_date"]
    timezone = data["timezone"]
    lessons = data["lessons"]

    index = select_lesson(start_date, timezone, len(lessons), override_day=args.day)
    lesson = lessons[index]

    site_url = os.environ.get("SITE_URL", "https://placeholder.github.io/cv-from-scratch/")

    payload = build_message(lesson, site_url)

    if args.dry_run:
        print("DRY RUN MODE. Message would be:")
        print(json.dumps(payload, indent=2))
        return

    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        print("Error: NTFY_TOPIC environment variable is missing.", file=sys.stderr)
        sys.exit(1)

    payload["topic"] = topic

    # Send POST request
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("https://ntfy.sh/", data=data_bytes, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("Notification sent successfully.")
            else:
                print(f"Failed to send notification. Status: {response.status}")
                sys.exit(1)
    except Exception as e:
        print(f"Exception during notification send: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()