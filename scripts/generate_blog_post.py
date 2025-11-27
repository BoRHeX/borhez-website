diff --git a/scripts/generate_blog_post.py b/scripts/generate_blog_post.py
index c71e2507fd38cd5f06a397244c7ebfbcefb02f23..f734e13aba60d78880a1cc713ea80e4c83df32c6 100644
--- a/scripts/generate_blog_post.py
+++ b/scripts/generate_blog_post.py
@@ -1,117 +1,153 @@
-diff --git a/scripts/generate_blog_post.py b/scripts/generate_blog_post.py
-index 86f3dfb8dc6e1fff6181235340a98750867ae91e..a72ab250cc5887e0c873db85b8a935e7dfff6878 100644
---- a/scripts/generate_blog_post.py
-+++ b/scripts/generate_blog_post.py
-@@ -63,104 +63,102 @@ def load_state():
- 
- def save_state(state):
-     with open(STATE_FILE, "w", encoding="utf-8") as f:
-         json.dump(state, f, indent=2, ensure_ascii=False)
- 
- def parse_date(dt_str):
-     try:
-         return datetime.date.fromisoformat(dt_str[:10])
-     except Exception:
-         return None
- 
- def recent_topics_from_state(state, cooldown_days):
-     cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
-     return {h["topic"] for h in state.get("history", []) if parse_date(h.get("date", "")) and parse_date(h.get("date", "")) >= cutoff}
- 
- def scan_existing_posts_for_topics(cooldown_days):
-     recent = set()
-     if not CONTENT_DIR.exists():
-         return recent
-     cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
-     for md in CONTENT_DIR.glob("*.md"):
-         try:
-             text = md.read_text(encoding="utf-8")
-             m = re.search(r"(?s)^---(.*?)---", text)
-             block = m.group(1) if m else ""
--            tm = re.search(r"(?im)^\s*topic\s*:\s*['"]?(.+?)['"]?\s*$", block)
--            dm = re.search(r"(?im)^\s*date\s*:\s*['"]?(\d{4}-\d{2}-\d{2}).*['"]?\s*$", block)
-+            # Extract topic from front matter with optional quotes and whitespace around the key and value.
-+            tm = re.search(r"(?im)^\s*topic\s*:\s*['\"]?(.*?)['\"]?\s*$", block)
-+            # Extract date in YYYY-MM-DD format from the front matter with optional quotes.
-+            dm = re.search(r"(?im)^\s*date\s*:\s*['\"]?(\d{4}-\d{2}-\d{2}).*['\"]?\s*$", block)
-             if tm and dm:
-                 t = tm.group(1).strip()
-                 d = parse_date(dm.group(1).strip())
-                 if d and d >= cutoff:
-                     recent.add(t)
-         except Exception:
-             continue
-     return recent
- 
- def choose_topic(topics, cooldown_days, state):
-     blocked = recent_topics_from_state(state, cooldown_days) | scan_existing_posts_for_topics(cooldown_days)
-     candidates = [t for t in topics if t not in blocked]
-     if candidates:
-         return random.choice(candidates)
-     used = {h["topic"]: parse_date(h.get("date", "1970-01-01")) or datetime.date(1970,1,1) for h in state.get("history", [])}
-     return sorted(topics, key=lambda t: used.get(t, datetime.date(1970,1,1)))[0]
- 
- def render_front_matter(title, topic, tags):
-     now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
--    fm = f"---
-+    fm = f"""---
- title: "{title}"
- date: {now_utc}
- draft: false
- tags: [{', '.join([json.dumps(t) for t in tags])}]
- categories: ["KBC"]
- topic: "{topic}"
- ---
--"
-+"""
-     return fm
- 
- def generate_body(topic):
-     paragraphs = [
-         f"{topic} in the Knowledge‑Based Currency (KBC) framework: a concise overview.",
-         "This post is auto‑generated as part of the daily knowledge log. It summarizes core principles and links them to practical implications for builders and curious readers.",
-         "Expect a richer, LLM‑expanded narrative in production runs when OPENAI_API_KEY is configured in repository secrets.",
-     ]
--    return "
--
--".join(paragraphs)
-+    return "\n\n".join(paragraphs)
- 
- def main():
-     ap = argparse.ArgumentParser()
-     ap.add_argument("--rotate", action="store_true", help="Enable topic rotation and recent-topic avoidance")
-     ap.add_argument("--cooldown-days", type=int, default=21, help="Do not repeat a topic within this many days")
-     args = ap.parse_args()
- 
-     topics = load_topics()
-     state = load_state()
- 
-     topic = choose_topic(topics, args.cooldown_days, state) if args.rotate else random.choice(topics)
- 
-     today = datetime.date.today()
-     nice = topic.replace("(", " — ").replace(")", "")
-     title = f"{nice} — Daily KBC Note ({today.isoformat()})"
-     slug = slugify(f"{today.isoformat()} {topic}")[:80]
- 
-     CONTENT_DIR.mkdir(parents=True, exist_ok=True)
-     path = CONTENT_DIR / f"{slug}.md"
-     idx = 2
-     while path.exists():
-         path = CONTENT_DIR / f"{slug}-{idx}.md"
-         idx += 1
- 
-     tags = ["Knowledge‑Based Currency", "KBC", topic.split(" ")[0]]
-     front = render_front_matter(title, topic, tags)
-     body = generate_body(topic)
--    path.write_text(front + "
--" + body + "
--", encoding="utf-8")
-+    path.write_text(front + "\n\n" + body + "\n", encoding="utf-8")
- 
-     state.setdefault("history", []).append({"topic": topic, "date": today.isoformat()})
-     state["history"] = state["history"][-180:]
-     save_state(state)
-     print(f"Generated: {path}")
- 
- if __name__ == "__main__":
-     main()
+#!/usr/bin/env python3
+import argparse
+import datetime
+import json
+import random
+import re
+import textwrap
+from pathlib import Path
+
+from slugify import slugify
+
+BASE_DIR = Path(__file__).resolve().parent.parent
+SCRIPT_DIR = Path(__file__).resolve().parent
+CONTENT_DIR = BASE_DIR / "content" / "posts"
+TOPICS_FILE = SCRIPT_DIR / "topics.json"
+STATE_FILE = SCRIPT_DIR / ".blog_state.json"
+
+
+def load_topics():
+    if not TOPICS_FILE.exists():
+        raise FileNotFoundError(f"Missing topics file: {TOPICS_FILE}")
+
+    data = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))
+    topics = data.get("topics", [])
+    if not topics:
+        raise ValueError("No topics found in topics.json")
+    return topics
+
+
+def load_state():
+    if STATE_FILE.exists():
+        with open(STATE_FILE, "r", encoding="utf-8") as f:
+            return json.load(f)
+    return {}
+
+
+def save_state(state):
+    with open(STATE_FILE, "w", encoding="utf-8") as f:
+        json.dump(state, f, indent=2, ensure_ascii=False)
+
+
+def parse_date(dt_str):
+    try:
+        return datetime.date.fromisoformat(dt_str[:10])
+    except Exception:
+        return None
+
+
+def recent_topics_from_state(state, cooldown_days):
+    cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
+    return {
+        h["topic"]
+        for h in state.get("history", [])
+        if parse_date(h.get("date", "")) and parse_date(h.get("date", "")) >= cutoff
+    }
+
+
+def scan_existing_posts_for_topics(cooldown_days):
+    recent = set()
+    if not CONTENT_DIR.exists():
+        return recent
+
+    cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
+    for md in CONTENT_DIR.glob("*.md"):
+        try:
+            text = md.read_text(encoding="utf-8")
+            m = re.search(r"(?s)^---(.*?)---", text)
+            block = m.group(1) if m else ""
+            # Extract topic from front matter with optional quotes and whitespace around the key and value.
+            tm = re.search(r"(?im)^\s*topic\s*:\s*['\"]?(.*?)['\"]?\s*$", block)
+            # Extract date in YYYY-MM-DD format from the front matter with optional quotes.
+            dm = re.search(r"(?im)^\s*date\s*:\s*['\"]?(\d{4}-\d{2}-\d{2}).*['\"]?\s*$", block)
+            if tm and dm:
+                t = tm.group(1).strip()
+                d = parse_date(dm.group(1).strip())
+                if d and d >= cutoff:
+                    recent.add(t)
+        except Exception:
+            continue
+    return recent
+
+
+def choose_topic(topics, cooldown_days, state):
+    blocked = recent_topics_from_state(state, cooldown_days) | scan_existing_posts_for_topics(cooldown_days)
+    candidates = [t for t in topics if t not in blocked]
+    if candidates:
+        return random.choice(candidates)
+
+    used = {h["topic"]: parse_date(h.get("date", "1970-01-01")) or datetime.date(1970, 1, 1) for h in state.get("history", [])}
+    return sorted(topics, key=lambda t: used.get(t, datetime.date(1970, 1, 1)))[0]
+
+
+def render_front_matter(title, topic, tags):
+    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
+    fm = textwrap.dedent(
+        f"""---
+        title: \"{title}\"
+        date: {now_utc}
+        draft: false
+        tags: [{', '.join([json.dumps(t) for t in tags])}]
+        categories: [\"KBC\"]
+        topic: \"{topic}\"
+        ---
+        """
+    )
+    return fm
+
+
+def generate_body(topic):
+    paragraphs = [
+        f"{topic} in the Knowledge‑Based Currency (KBC) framework: a concise overview.",
+        "This post is auto‑generated as part of the daily knowledge log. It summarizes core principles and links them to practical implications for builders and curious readers.",
+        "Expect a richer, LLM‑expanded narrative in production runs when OPENAI_API_KEY is configured in repository secrets.",
+    ]
+    return "\n\n".join(paragraphs)
+
+
+def main():
+    ap = argparse.ArgumentParser()
+    ap.add_argument("--rotate", action="store_true", help="Enable topic rotation and recent-topic avoidance")
+    ap.add_argument("--cooldown-days", type=int, default=21, help="Do not repeat a topic within this many days")
+    args = ap.parse_args()
+
+    topics = load_topics()
+    state = load_state()
+
+    topic = choose_topic(topics, args.cooldown_days, state) if args.rotate else random.choice(topics)
+
+    today = datetime.date.today()
+    nice = topic.replace("(", " — ").replace(")", "")
+    title = f"{nice} — Daily KBC Note ({today.isoformat()})"
+    slug = slugify(f"{today.isoformat()} {topic}")[:80]
+
+    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
+    path = CONTENT_DIR / f"{slug}.md"
+    idx = 2
+    while path.exists():
+        path = CONTENT_DIR / f"{slug}-{idx}.md"
+        idx += 1
+
+    tags = ["Knowledge‑Based Currency", "KBC", topic.split(" ")[0]]
+    front = render_front_matter(title, topic, tags)
+    body = generate_body(topic)
+    path.write_text(front + "\n\n" + body + "\n", encoding="utf-8")
+
+    state.setdefault("history", []).append({"topic": topic, "date": today.isoformat()})
+    state["history"] = state["history"][-180:]
+    save_state(state)
+    print(f"Generated: {path}")
+
+
+if __name__ == "__main__":
+    main()
