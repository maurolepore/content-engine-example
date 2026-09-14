# [Content Engine](https://youtu.be/QRXJ-9yPb0w?si=_OIkIXQxCbS2udmp) from [@Maxjohnscn](https://www.youtube.com/@Maxjohnscn/videos)'s [demo](https://www.youtube.com/watch?v=QRXJ-9yPb0w) ([guide](https://drive.google.com/file/d/1b-Sch9iZNhscDapJ69tEs06Tc7Xt896b/view))
https://www.linkedin.com/in/max-johnson-briix/

Pipeline:
- Research (web search via Google News RSS + topic synthesis).
- Score (by relevance / timeliness / angle freshness).
- Write hooks and scripts.

Run the pipeline with:
```python
python3 -m src.run
```

See the results at http://localhost:8080

------

I built everything in about 1h with [OpenCode](https://opencode.ai/) and Kimi K3 as the manager agent, using Max's prompts verbatim (except for an additional fix commit: `ffa042b`). I used my [OpenCode Go](https://opencode.ai/go) subscription and spent ~100K tokens and USD 2.4.

Each run of the pipeline uses `openai/gpt-oss-120b` using my [`GROQ_API_KEY`](https://console.groq.com/keys) (free tier).