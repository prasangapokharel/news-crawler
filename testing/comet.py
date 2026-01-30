import os
import requests
from dotenv import load_dotenv

load_dotenv()


def test_comet_api():
    print("=" * 60)
    print("COMET API TEST")
    print("=" * 60)
    print()

    api_key = os.getenv("COMET_API_KEY")
    api_url = os.getenv("COMET_ANTROPIC_URL")
    model = os.getenv("COMET_MODEL")

    print(f"API URL: {api_url}")
    print(f"Model: {model}")
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: NOT FOUND")
    print()

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with a short greeting to confirm the API is working.",
            }
        ],
    }

    print("-> Sending test request...")

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        print(f"Status Code: {response.status_code}")
        print()

        if response.status_code == 200:
            data = response.json()
            print("API Response:")
            print("-" * 60)
            if "content" in data and len(data["content"]) > 0:
                text = data["content"][0]["text"]
                print(text.encode("ascii", "ignore").decode("ascii"))
            else:
                print(str(data).encode("ascii", "ignore").decode("ascii"))
            print("-" * 60)
            print()
            print("COMET API TEST PASSED!")
        else:
            print("Error Response:")
            print(response.text)
            print()
            print("COMET API TEST FAILED!")

    except Exception as e:
        print(f"Exception: {e}")
        print()
        print("COMET API TEST FAILED!")

    print()
    print("=" * 60)


if __name__ == "__main__":
    test_comet_api()
