/* Reads /api/latest on load + on Refresh click. Pure render, staggered in. */

const $ = (sel) => document.querySelector(sel);
let staggerBase = 0; // keeps animation delays consistent across sections

function formatTs(ts) {
  try { return new Date(ts).toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" }); }
  catch { return ts; }
}

function rise(el, i) {
  el.classList.add("rise");
  el.style.animationDelay = `${staggerBase + i * 45}ms`;
}

function renderTopics(scored) {
  const ol = $("#topics");
  ol.innerHTML = "";
  const top = scored[0];
  scored.forEach((t, i) => {
    const li = document.createElement("li");
    li.className = "topic" + (t === top ? " topic--winner" : "");
    const dims = ["relevance", "timeliness", "angle_freshness"]
      .map((d) => t[d] ? `<span class="dim">${d.replace("_", " ")} <span class="dim__score">${t[d].score}</span></span>` : "")
      .join("");
    li.innerHTML = `
      <span class="topic__idx">${String(i + 1).padStart(2, "0")}</span>
      <div>
        <span class="topic__name">${t.topic}</span>
        ${t === top ? '<span class="tag">LOCKED-IN</span>' : ""}
        <div class="topic__dims">${dims}</div>
      </div>
      <div class="meter">
        <div class="meter__bar"><div class="meter__fill" style="width:${t.overall * 10}%"></div></div>
        <span class="meter__score">${t.overall?.toFixed(1)}</span>
      </div>`;
    rise(li, i);
    ol.appendChild(li);
  });
  staggerBase = scored.length * 45;
  $("#topics-meta").textContent = `${scored.length} SCORED`;
}

function renderHooks(hooks, strongest) {
  const wrap = $("#hooks");
  wrap.innerHTML = "";
  hooks.forEach((text, i) => {
    const btn = document.createElement("button");
    btn.className = "hook";
    const flag = text === strongest ? '<span class="hook__flag">STRONGEST</span>' : "";
    btn.innerHTML = `<span class="hook__num">HOOK_${i + 1}</span>${flag}${text}`;
    btn.onclick = () => {
      wrap.querySelectorAll(".hook").forEach((h) => h.classList.remove("selected"));
      btn.classList.add("selected");
    };
    if (text === strongest) btn.classList.add("selected");
    rise(btn, i);
    wrap.appendChild(btn);
  });
}

function renderScript(script) {
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
  $("#script-meta").textContent = `${script.length} SECTIONS`;
}

async function load() {
  staggerBase = 0;
  let data;
  try {
    const res = await fetch("/api/latest", { cache: "no-store" });
    data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || "no data");
  } catch {
    $("#timestamp").textContent = "NO RUNS YET";
    $("#empty").classList.remove("hidden");
    return;
  }
  $("#empty").classList.add("hidden");
  $("#timestamp").textContent = `RUN ${formatTs(data.timestamp)}`;
  renderTopics(data.scored_topics || []);
  renderHooks(data.hooks || [], data.strongest_hook);
  renderScript(data.script || []);
}

$("#refresh").addEventListener("click", load);
load();
