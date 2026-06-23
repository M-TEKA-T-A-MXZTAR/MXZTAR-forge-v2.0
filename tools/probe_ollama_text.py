#!/usr/bin/env python3
"""
Probe local Ollama text generation through the HTTP API.

Purpose:
- confirm Ollama responds
- confirm qwen2.5vl:3b is usable
- enforce hardware-kind defaults
- avoid UI wiring until the backend is proven
"""

import json
import os

import requests


MODEL = "qwen2.5vl:3b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def main() -> int:
    os.environ["OLLAMA_NUM_THREAD"] = "2"
    os.environ["OLLAMA_NUM_PARALLEL"] = "1"

    payload = {
        "model": MODEL,
        "prompt": (
            "Reply with exactly one short sentence confirming you are ready "
            "for MXZTAR-forge source-art workflow testing."
        ),
        "stream": False,
        "options": {
            "num_thread": 2,
            "temperature": 0.2,
            "num_predict": 80,
        },
    }

    print("MXZTAR-forge Ollama HTTP Probe")
    print(f"Model: {MODEL}")
    print("Policy: OLLAMA_NUM_THREAD=2, OLLAMA_NUM_PARALLEL=1")
    print(f"URL: {OLLAMA_URL}")
    print()

    try:
        resp = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180,
        )
        resp.raise_for_status()
        body = resp.text
    except requests.exceptions.RequestException as exc:
        print("FAIL: could not reach Ollama HTTP API.")
        print(exc)
        print()
        print("Check whether Ollama is running:")
        print("  systemctl --user status ollama")
        print("or:")
        print("  ollama serve")
        return 1

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        print("FAIL: Ollama returned non-JSON response.")
        print(body)
        return 1

    if "error" in parsed:
        print("FAIL: Ollama returned an error.")
        print(parsed["error"])
        return 1

    response_text = str(parsed.get("response", "")).strip()

    if not response_text:
        print("FAIL: Ollama returned no response text.")
        print(parsed)
        return 1

    print("Response:")
    print(response_text)
    print()
    print("PASS: Ollama HTTP API completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
