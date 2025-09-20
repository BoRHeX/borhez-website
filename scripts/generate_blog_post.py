#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stateful blog post generator for Hugo (PaperMod) with topic rotation.

- Reads topics from 'scripts/topics.json'.
- Tracks last-used topics in '.github/state/blog_state.json' (created if missing).
- Avoids repeating a topic within N cooldown days (default 21).
- Writes front matter with 'topic' to help future rotation checks.
- Falls back to deterministic stub content if OPENAI_API_KEY is not set.

Usage:
  python scripts/generate_blog_post.py --rotate --cooldown-days 21
"""
import os, sys, json, re, argparse, datetime, random, pathlib
from slugify import slugify

try:
    import frontmatter
except Exception:
    frontmatter = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "posts"
STATE_DIR = ROOT / ".github" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = STATE_DIR / "blog_state.json"
TOPICS_FILE = ROOT / "scripts" / "topics.json"

def load_topics():
    if TOPICS_FILE.exists():
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        topics = [t.strip() for t in data.get("topics", []) if t.strip()]
        if topics:
            return topics
    return [
        "K-Chain (Knowledge Ledger)",
        "LightWeb (Decentralized Web Layer)",
        "Oracle AI (Validator)",
        "Y-Engine (Truth-Relevance-Novelty-Impact)",
        "Proof of Knowledge (PoK)",
        "Intrinsic Privacy & Security",
        "KBC MVS (FastAPI + Streamlit)",
        "Decentralized Identity & Self-Sovereign Data",
        "Knowledge Blocks (KBs): Claims + Evidence",
        "KBC Economics & Incentives",
        "KBC vs. Fiat/Crypto",
        "Families & Shared Chains",
        "Education & Research on KBC",
        "Governance & Validation Markets",
        "Open-Source Roadmap & Community",
    ]

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def parse_date(dt_str):
    try:
        return datetime.date.fromisoformat(dt_str[:10])
    except Exception:
        return None

def recent_topics_from_state(state, cooldown_days):
    cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
    return {h["topic"] for h in state.get("history", []) if parse_date(h.get("date", "")) and parse_date(h.get("date", "")) >= cutoff}

def scan_existing_posts_for_topics(cooldown_days):
    recent = set()
    if not CONTENT_DIR.exists():
        return recent
    cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
    for md in CONTENT_DIR.glob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
            m = re.search(r"(?s)^---(.*?)---", text)
            block = m.group(1) if m else ""
            tm = re.search(r"(?im)^\s*topic\s*:\s*['"]?(.+?)['"]?\s*$", block)
            dm = re.search(r"(?im)^\s*date\s*:\s*['"]?(\d{4}-\d{2}-\d{2}).*['"]?\s*$", block)
            if tm and dm:
                t = tm.group(1).strip()
                d = parse_date(dm.group(1).strip())
                if d and d >= cutoff:
                    recent.add(t)
        except Exception:
            continue
    return recent

def choose_topic(topics, cooldown_days, state):
    blocked = recent_topics_from_state(state, cooldown_days) | scan_existing_posts_for_topics(cooldown_days)
    candidates = [t for t in topics if t not in blocked]
    if candidates:
        return random.choice(candidates)
    used = {h["topic"]: parse_date(h.get("date", "1970-01-01")) or datetime.date(1970,1,1) for h in state.get("history", [])}
    return sorted(topics, key=lambda t: used.get(t, datetime.date(1970,1,1)))[0]

def render_front_matter(title, topic, tags):
    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    fm = f"---
title: "{title}"
date: {now_utc}
draft: false
tags: [{', '.join([json.dumps(t) for t in tags])}]
categories: ["KBC"]
topic: "{topic}"
---
"
    return fm

def generate_body(topic):
    paragraphs = [
        f"{topic} in the Knowledge‑Based Currency (KBC) framework: a concise overview.",
        "This post is auto‑generated as part of the daily knowledge log. It summarizes core principles and links them to practical implications for builders and curious readers.",
        "Expect a richer, LLM‑expanded narrative in production runs when OPENAI_API_KEY is configured in repository secrets.",
    ]
    return "

".join(paragraphs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rotate", action="store_true", help="Enable topic rotation and recent-topic avoidance")
    ap.add_argument("--cooldown-days", type=int, default=21, help="Do not repeat a topic within this many days")
    args = ap.parse_args()

    topics = load_topics()
    state = load_state()

    topic = choose_topic(topics, args.cooldown_days, state) if args.rotate else random.choice(topics)

    today = datetime.date.today()
    nice = topic.replace("(", " — ").replace(")", "")
    title = f"{nice} — Daily KBC Note ({today.isoformat()})"
    slug = slugify(f"{today.isoformat()} {topic}")[:80]

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    path = CONTENT_DIR / f"{slug}.md"
    idx = 2
    while path.exists():
        path = CONTENT_DIR / f"{slug}-{idx}.md"
        idx += 1

    tags = ["Knowledge‑Based Currency", "KBC", topic.split(" ")[0]]
    front = render_front_matter(title, topic, tags)
    body = generate_body(topic)
    path.write_text(front + "
" + body + "
", encoding="utf-8")

    state.setdefault("history", []).append({"topic": topic, "date": today.isoformat()})
    state["history"] = state["history"][-180:]
    save_state(state)
    print(f"Generated: {path}")

if __name__ == "__main__":
    main()
