/* Displays a run from /api/latest. Click a topic → its hooks; click a hook → its script.
   Read-only: never triggers the pipeline. */

const $ = (sel) => document.querySelector(sel);
let data = null;
let selectedTopic = 0; // index into scored_topics (rank 0 always carries LOCKED-IN)
let selectedHook = 0; // index into the selected topic's hooks (always matches shown script)
let staggerBase = 0;

function formatTs(ts) {
  try { return new Date(ts).toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return ts; }
}

function rise(el, i) {
  el.classList.add("rise");
  el.style.animationDelay = `${staggerBase + i * 45}ms`;
}

function renderTopics() {
  const scored = data.scored_topics || [];
  const ol = $("#topics");
  ol.innerHTML = "";
  scored.forEach((t, i) => {
    const li = document.createElement("li");
    li.className = "topic" + (i === 0 ? " topic--winner" : "") + (i === selectedTopic ? " selected" : "");
    const dims = ["relevance", "timeliness", "angle_freshness"]
      .map((d) => t[d] ? `<span class="dim">${d.replace("_", " ")} <span class="dim__score">${t[d].score}</span></span>` : "")
      .join("");
    li.innerHTML = `
      <span class="topic__idx">${String(i + 1).padStart(2, "0")}</span>
      <div>
        <span class="topic__name">${t.topic}</span>
        ${i === 0 ? '<span class="tag">LOCKED-IN</span>' : ""}
        <div class="topic__dims">${dims}</div>
      </div>
      <div class="meter">
        <div class="meter__bar"><div class="meter__fill" style="width:${t.overall * 10}%"></div></div>
        <span class="meter__score">${t.overall?.toFixed(1)}</span>
      </div>`;
    li.onclick = () => {
      selectedTopic = i;
      selectedHook = 0;
      renderTopics();
      renderHooks();
      renderScript();
    };
    rise(li, i);
    ol.appendChild(li);
  });
  staggerBase = scored.length * 45;
  $("#topics-meta").textContent = `${scored.length} SCORED`;
}

function renderHooks() {
  const topic = data.scored_topics[selectedTopic];
  const hooks = (topic && topic.hooks) || [];
  const wrap = $("#hooks");
  wrap.innerHTML = "";
  hooks.forEach((text, i) => {
    const btn = document.createElement("button");
    btn.className = "hook" + (i === selectedHook ? " selected" : "");
    const flag = text === topic.strongest ? '<span class="hook__flag">STRONGEST</span>' : "";
    btn.innerHTML = `<span class="hook__num">HOOK_${i + 1}</span>${flag}${text}`;
    btn.onclick = () => {
      selectedHook = i;
      renderHooks();
      renderScript();
    };
    rise(btn, i);
    wrap.appendChild(btn);
  });
}

function renderScript() {
  const topic = data.scored_topics[selectedTopic];
  const script = (topic && topic.scripts && topic.scripts[selectedHook]) || [];
  const wrap = $("#script");
  wrap.innerHTML = "";
  script.forEach((s, i) => {
    const div = document.createElement("div");
    div.className = "script-section";
    div.innerHTML = `
      <div class="script-section__label">${s.section}</div>
      <div class="script-section__text"></div>`;
    div.querySelector(".script-section__text").textContent = s.text;
    rise(div, i);
    wrap.appendChild(div);
  });
  $("#script-meta").textContent =
    `${topic ? topic.topic.toUpperCase().slice(0, 28) : ""} · HOOK_${selectedHook + 1} · ${script.length} SECTIONS`;
}

async function load() {
  staggerBase = 0;
  let payload;
  try {
    const res = await fetch("/api/latest", { cache: "no-store" });
    payload = await res.json();
    if (!res.ok || payload.error || !payload.scored_topics) throw new Error(payload.error || "no data");
  } catch {
    $("#timestamp").textContent = "NO RUNS YET";
    $("#empty").classList.remove("hidden");
    return;
  }
  $("#empty").classList.add("hidden");
  data = payload;
  selectedTopic = 0;
  selectedHook = 0;
  $("#timestamp").textContent = `RUN ${formatTs(data.timestamp)}`;
  renderTopics();
  renderHooks();
  renderScript();
}

$("#refresh").addEventListener("click", load);
load();
