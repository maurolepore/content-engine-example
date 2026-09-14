# Content engine

## Example

- [Demo](https://youtu.be/QRXJ-9yPb0w?si=yyiC0rOawaeSRx4I)
- [Guide](https://drive.google.com/file/d/1b-Sch9iZNhscDapJ69tEs06Tc7Xt896b/view)

## Usage

The pipeline lives in `src/`, one module per stage. Zero dependencies
(stdlib only); needs `GROQ_API_KEY` in the environment.

- Research (web search via Google News RSS + topic synthesis):
  `python3 -m src.research`
- Scoring (rubric: relevance / timeliness / angle freshness, vs `audience.md`):
  `python3 -m src.score`
- Writing (3 hooks per topic vs `voice-rules.md`, each expanded into its own
  script vs `sample-scrtipts-file.md` — 15 scripts per run): `python3 -m src.write`
- Full pipeline (everything above, one timestamped JSON into `/output`):
  `python3 -m src.run`
- Dashboard (displays latest `/output` file at http://localhost:8080):
  `python3 -m src.dashboard`

Each run prints a compact leaderboard plus the winning topic and chosen hook.
The dashboard is display-only — Refresh re-reads `/output`, it never triggers
the pipeline.

