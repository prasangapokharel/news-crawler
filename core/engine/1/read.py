from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).resolve().parents[3]


def read_md(rel_path):
    return (BASE / rel_path).read_text(encoding="utf-8").strip()


def get_system_prompt():
    focus = read_md("core/engine/1/source/keyword/focus.md")
    keywords = read_md("core/engine/1/source/keyword/word.md")
    social = read_md("core/engine/1/source/social/social.md")
    brain = read_md("core/engine/2/brain/brain.md")

    return f"""You are a Crawler for News Websites — daily edition

Focus (in strict priority order):
{focus}

Keywords to watch:
{keywords}

Social channels / pages / accounts to monitor:
{social}

{brain}
"""
