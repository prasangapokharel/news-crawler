from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[3]


def save_response(content, focus_summary=None):
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H-%M-%S")

    alert_dir = BASE / "alert" / today
    alert_dir.mkdir(parents=True, exist_ok=True)

    file_path = alert_dir / f"news_{timestamp}.md"

    formatted_content = format_response(content, today, timestamp, focus_summary)

    file_path.write_text(formatted_content, encoding="utf-8")

    return file_path


def format_response(content, date, time, focus_summary=None):
    if not focus_summary:
        focus_summary = get_focus_summary()

    header = f"""# Nepal News Crawler Report
**Date:** {date}
**Time:** {time.replace("-", ":")}
**Focus:** {focus_summary}

---

"""
    return header + content


def get_focus_summary():
    focus_file = BASE / "core" / "engine" / "1" / "source" / "keyword" / "focus.md"
    focus_content = focus_file.read_text(encoding="utf-8").strip()
    lines = [
        line.strip("- ").split("(")[0].strip()
        for line in focus_content.split("\n")
        if line.strip().startswith("-")
    ]
    return ", ".join(lines[:3]) if lines else "Nepal News"
