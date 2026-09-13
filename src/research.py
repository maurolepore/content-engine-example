"""Stage 1 of the pipeline: search the web, then synthesise trending topics.

DuckDuckGo gathers raw search hits; Groq turns them into structured topics.
Run `python3 -m src.research` to see the raw output for both halves.
"""

import json

from . import config, llm, search

PROMPT = """Here are web search results about {space}, collected today.

{numbered_results}

Synthesise {count} distinct trending topics from these results.
Return a JSON array. Each item must have exactly these fields:
- "topic": short title of the trend (a few words)
- "summary": 1-2 sentences on what is actually happening
- "result_indices": array of the result numbers this topic is based on

Return ONLY the JSON array. No markdown fences, no commentary."""


def research():
    queries = search.search_all(config.QUERIES)

    flat = []
    for q in queries:
        flat.extend(r for r in q["results"] if r not in flat)
    numbered = "\n".join(
        f"[{i+1}] {r['title']} ({r['source']}, {r['date']})"
        for i, r in enumerate(flat)
    )
    raw = llm.chat(
        [
            {
                "role": "user",
                "content": PROMPT.format(
                    space=config.SPACE, numbered_results=numbered, count=config.TOPIC_COUNT
                ),
            }
        ]
    )
    topics = _parse_json_array(raw)
    if topics is None:
        raise ValueError(f"model did not return a JSON array:\n{raw}")
    return {"search": queries, "results": flat, "topics": topics}


def _parse_json_array(text):
    """Best-effort extraction of a JSON array from model output."""
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def main():
    print(json.dumps(research(), indent=2))


if __name__ == "__main__":
    main()
