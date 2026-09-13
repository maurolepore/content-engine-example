PROMPT 1 — Kickoff
I want to build an autonomous content agent called Content Engine. It should:
1. Read my personal knowledge base from a /knowledge folder (voice-rules.md,
   about-me-file.md, audience.md, sample-scripts.md)
2. Search the web for trending topics in the AI/automation/entrepreneurship space
3. Score each topic against a rubric: relevance to my audience (using
   audience.md), timeliness, and how saturated the angle already is —
   output a 1-10 score with a one-line reason for each
4. Take the top-scored topic and draft 3 hook options in my voice
   (using voice-rules.md)
5. Expand the strongest hook into a full short-form video script following
   the structure and tone of my example scripts (using sample-scripts.md)
6. Save the full output (topics, scores, hooks, script) as a single
   structured JSON file in /output, one file per run, timestamped
Set this up as a clean, simple project. Build and test the research step
first — I want to see each stage working before we move to the next one,
not get a black box at the end.

PROMPT 2 — Research + scoring
Now build and test the research and scoring step end to end. Run it live
against knowledge/audience.md and show me the raw scored output for a real
topic search before we move on — I want to see the actual scores and
reasoning, not a mocked example.

PROMPT 3 — Hooks + script
Now build the hook and script generation step. Take the top-scored topic
from the last run, generate 3 hook options in my voice using
knowledge/voice-rules.md, then expand the strongest one into a full script
using knowledge/sample-scripts.md as the pattern for structure and pacing.
Save all of it into the same run's JSON output.

PROMPT 4 — Wire it into one command
Wire research, scoring, hook writing, and script writing into a single
command that runs the whole pipeline end to end with no manual steps in
between, and writes one clean JSON file to /output when it's done.

PROMPT 5 — The dashboard
Build a local dashboard that reads the latest JSON file from /output and
displays it. This needs to look genuinely designed, not like a generic
AI-generated dashboard — no purple gradients, no Inter/Arial/system fonts,
no centered-card-on-white-background templates.

Direction: dark, technical, "operator's terminal" feel — near-black
background, one sharp accent color, a distinctive monospace or condensed
display font paired with a clean readable body font. Treat it like a
mission-control readout, not a SaaS landing page.

Structure:
- Header: run timestamp + a "Refresh" button that just re-reads the latest
  file from /output — this dashboard only displays results, it doesn't
  trigger the pipeline itself (that happens separately, from the terminal)
- A ranked list of the researched topics with scores shown as bars/meters,
  the winning topic visually distinct from the rest
- The 3 hook options for the winning topic, shown as selectable cards
- The full script, clearly laid out, with its structure (hook / problem /
  mechanism / proof / CTA) visually separated into sections
- A subtle staggered load-in animation when new data appears — no
  spinners, no loading skeletons

Use CSS variables for the whole color system so it's easy to reskin later.
Make it look like something designed on purpose, not a default template.
