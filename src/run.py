"""One command: research + scoring + hooks + script, saved to /output.

`python3 -m src.run` runs the full pipeline with no manual steps and writes
`output/run-YYYYMMDD-HHMMSS.json`. The console prints a compact leaderboard.
"""

import json
from datetime import datetime
from pathlib import Path

from . import write

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


def main():
    timestamp = datetime.now()
    path = OUTPUT_DIR / f"run-{timestamp:%Y%m%d-%H%M%S}.json"

    result = {"timestamp": timestamp.isoformat(), **write.run()}

    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    scored = result["scored_topics"]
    top = scored[0]
    scripts_total = sum(len(t["scripts"]) for t in scored)
    print(f"\n{len(result['results'])} sources scanned, {len(scored)} topics scored\n")
    for t in scored:
        print(f"  {t['overall']:<4} {t['topic']} ({len(t['hooks'])} hooks, {len(t['scripts'])} scripts)")
    print(f"\nWinning topic: {top['topic']}")
    print(f"Strongest hook: {top['strongest']}")
    print(f"{scripts_total} scripts across {len(scored)} topics")
    print(f"\nSaved → {path}")


if __name__ == "__main__":
    main()
