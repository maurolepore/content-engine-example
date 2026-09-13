"""Stage 3 of the pipeline: hooks in the creator's voice, then a full script.

- hooks(): 3 hook options for the top topic, judged against knowledge/voice-rules.md
- script(): expands the strongest hook using knowledge/sample-scrtipts-file.md
  as the structure/pacing pattern

Run `python3 -m src.write` for the full research + scoring + writing output.
"""

import json

from . import knowledge, llm, score

HOOKS_PROMPT = """Write hooks for a short-form video. Voice rules of the creator:

VOICE RULES:
{voice}

TOPIC to hook: "{topic_title}" — {topic_summary}

Write exactly 3 hook options openers, each a single sentence.
Return a JSON object with fields:
- "hooks": array of 3 strings
- "strongest_index": 0-based index of the strongest hook
Return ONLY the JSON object. No markdown fences, no commentary."""

SCRIPT_PROMPT = """Write a short-form video script (~30-45 seconds) expanding the hook below.

CREATOR'S VOICE RULES:
{voice}

STRUCTURE AND PACING PATTERN (from the creator's sample scripts):
{samples}

TOPIC: "{topic_title}" — {topic_summary}
HOOK to open with: "{hook}"

Write the script as a JSON array of labelled sections, where each section is
{{"section": label, "text": spoken lines}}. Use this structure:
HOOK / PROBLEM / MECHANISM / PROOF / CTA
Return ONLY the JSON array. No markdown fences, no commentary."""


def hooks(topic, kb):
    raw = llm.chat(
        [
            {
                "role": "user",
                "content": HOOKS_PROMPT.format(
                    voice=kb["voice"],
                    topic_title=topic["topic"],
                    topic_summary=topic["summary"],
                ),
            }
        ]
    )
    out = _parse(raw)
    if not out or "hooks" not in out:
        raise ValueError(f"model did not return hooks JSON:\n{raw}")
    return {
        "options": out["hooks"],
        "strongest": out["hooks"][out["strongest_index"]],
    }


def script(topic, hook, kb):
    raw = llm.chat(
        [
            {
                "role": "user",
                "content": SCRIPT_PROMPT.format(
                    voice=kb["voice"],
                    samples=kb["samples"],
                    topic_title=topic["topic"],
                    topic_summary=topic["summary"],
                    hook=hook,
                ),
            }
        ]
    )
    sections = _parse(raw)
    if not sections:
        raise ValueError(f"model did not return script JSON:\n{raw}")
    return sections


def _parse(text):
    """Return the first JSON array/object in model output, else None."""
    if "{" in text and ("[" not in text or text.find("{") < text.find("[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def run():
    """Stages 1-3 end to end: research, score, hooks, script."""
    kb = knowledge.load_all()
    out = score.run()
    top = out["scored_topics"][0]
    hook_out = hooks(top, kb)
    out["hooks"] = hook_out["options"]
    out["strongest_hook"] = hook_out["strongest"]
    out["script"] = script(top, hook_out["strongest"], kb)
    return out


def main():
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()
