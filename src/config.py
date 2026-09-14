"""Central configuration for the Content Engine pipeline."""

LLM_MODEL = "openai/gpt-oss-120b"

# The space the research step scans for trending topics.
SPACE = "AI, automation, and entrepreneurship"

# DuckDuckGo queries the research step runs each time.
QUERIES = [
    "AI automation trends 2026 business owners",
    "AI news entrepreneurs this week",
    "AI tools small business practical 2026",
    "AI agency entrepreneurship news this week",
]

# How many candidate topics the research step returns per run.
# Three hooks and three scripts are expanded for every topic.
TOPIC_COUNT = 5
