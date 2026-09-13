"""Loads the personal knowledge base from /knowledge."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"

FILES = {
    "about": "about-me.md",
    "audience": "audience.md",
    "voice": "voice-rules.md",
    "samples": "sample-scrtipts-file.md",
}


def load_all() -> dict:
    """Return every knowledge file as {key: markdown_text}."""
    out = {}
    for key, filename in FILES.items():
        path = KNOWLEDGE_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"missing knowledge file: {path}")
        out[key] = path.read_text(encoding="utf-8")
    return out
