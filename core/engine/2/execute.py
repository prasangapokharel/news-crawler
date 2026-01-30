import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def execute(system_prompt, user_message, scraped_content=None):
    api_key = os.getenv("COMET_API_KEY")
    api_url = os.getenv("COMET_ANTROPIC_URL")
    model = os.getenv("COMET_MODEL")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    if scraped_content:
        full_message = f"""{user_message}

SCRAPED HEADLINES WITH SOURCE LINKS:
{scraped_content}

Review all headlines above and verify which ones match the focus priorities. Include source links for verification."""
    else:
        full_message = user_message

    payload = {
        "model": model,
        "max_tokens": 8192,
        "system": system_prompt,
        "messages": [{"role": "user", "content": full_message}],
    }

    response = requests.post(api_url, headers=headers, json=payload, timeout=180)

    if response.status_code == 200:
        data = response.json()
        return data["content"][0]["text"]
    else:
        raise Exception(f"Comet API Error: {response.status_code} - {response.text}")
