"""Thin Groq chat-completions client (OpenAI-compatible, stdlib only)."""

import json
import os
import sys
import time
import urllib.error
import urllib.request

from . import config

_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def chat(messages, model=None, temperature=0.3):
    """Send messages, return assistant content string."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        sys.exit("GROQ_API_KEY is not set in the environment.")
    payload = {
        "model": model or config.LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    req = urllib.request.Request(
        _API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "content-engine/0.1",
        },
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.load(resp)
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"Groq API error {e.code}: {body}")
