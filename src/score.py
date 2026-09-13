"""Stage 2 of the pipeline: score researched topics against a rubric.

- relevance (1-10): fit for the audience in knowledge/audience.md
- timeliness (1-10): how current the trend is right now
- angle_freshness (1-10): 10 = fresh/unsaturated angle, 1 = played out

Run `python3 -m src.score` for the full research + scoring output.
"""

import json

from . import config, knowledge, llm, research

PROMPT = """You are scoring trending topics for a short-form video creator.

AUDIENCE (from the creator's knowledge base):
{audience}

TOPICS to score:
{topics}

Score each topic on three dimensions, 1-10 each:
- relevance: how well it fits this audience
- timeliness: how current it is right now
- angle_freshness: how unsaturated the angle is (10 = fresh, 1 = played out)

Return a JSON array, one object per topic, in the same order. Fields:
- "topic": exact topic title from the input
- "relevance": {{"score": int, "reason": one line}}
- "timeliness": {{"score": int, "reason": one line}}
- "angle_freshness": {{"score": int, "reason": one line}}
- "overall": float, mean of the three scores, rounded to 1 decimal

Return ONLY the JSON array. No markdown fences, no commentary."""


def score(topics):
    audience = knowledge.load_all()["audience"]
    topic_lines = "\n".join(
        f'- "{t["topic"]}" — {t["summary"]}' for t in topics
    )
    raw = llm.chat(
        [
            {
                "role": "user",
                "content": PROMPT.format(audience=audience, topics=topic_lines),
            }
        ]
    )
    scored = _parse(raw)
    if scored is None:
        raise ValueError(f"model did not return a JSON array:\n{raw}")
    for item in scored:
        match = next((t for t in topics if t["topic"] == item["topic"]), {})
        item.setdefault("summary", match.get("summary", ""))
    return sorted(scored, key=lambda t: t.get("overall", 0), reverse=True)


def _parse(text):
    """Return the first JSON array found in model output, else None."""
    start, end = text.find("[") if "[" in text else 0, text.rfind("]")
    if end == -1 or (start == -1 or start > end):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def run():
    """Full stage 1 + stage 2, returning everything."""
    research_out = research.research()
    scored = {"scored_topics": score(research_out["topics"])}
    research_out.update(scored)
    return research_out


def main():
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()
