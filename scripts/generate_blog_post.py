#!/usr/bin/env python3
"""
Generate a daily blog post for the KBC site.

- Uses CHAT_SUMMARY_PATH if available to summarize a recent KBC interaction.
- Otherwise generates a post from a rotating KBC topic list.
- Outputs a Markdown file in content/posts with proper Hugo front matter.
"""

import os
import random
import datetime
from pathlib import Path
from slugify import slugify
import openai


# ---- CONFIG ----
MODEL = "gpt-4"  # Can be 'gpt-4', 'gpt-4o', or 'gpt-3.5-turbo'
TOKENS = 1200
TEMPERATURE = 0.7


# ---- SETUP ----
def get_openai_client() -> "openai":
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("❌ OPENAI_API_KEY not set in environment.")
    openai.api_key = api_key
    return openai


# ---- CONTEXT ----
def read_chat_summary() -> str | None:
    path = os.environ.get("CHAT_SUMMARY_PATH")
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️ Failed to read chat summary from {path}: {e}")
        return None


def choose_topic(index: int = None) -> str:
    topics = [
        "the philosophy behind Knowledge‑Based Currency",
        "how the K‑Chain ensures trust and immutability",
        "the vision of LightWeb as a decentralized knowledge internet",
        "the role of Oracle AI in validating and synthesizing knowledge",
        "building the Minimum Viable System for KBC",
        "how knowledge becomes a universal asset",
        "why KBC matters for science and innovation",
        "the future of decentralized learning and value",
        "the link between KBC and education reform",
        "the difference between information and knowledge",
        "the ethics of valuing knowledge digitally",
        "resisting manipulation through verifiable truth",
        "KBC as a unifying system for human potential",
        "how to participate in the KBC ecosystem",
        "the mathematics of KBC and the 1 = ∑vi principle",
    ]
    return topics[index % len(topics)] if index is not None else random.choice(topics)


# ---- GENERATION ----
def generate_post(topic: str, client: "openai", summary: str | None) -> str:
    today = datetime.date.today().strftime("%B %d, %Y")
    if summary:
        prompt = (
            f"You are the official technical writer for the Knowledge-Based Currency (KBC) project.\n"
            f"Write a 600-word blog post for {today} summarizing today's development and insights in the project.\n"
            f"Use the following as your context and notes:\n{summary}\n\n"
            f"The post must be inspirational, intelligent, and accessible to curious readers. "
            f"Do not include YAML front matter, code fences, or markdown headers. Just write a plain text article with paragraphs and structure."
        )
    else:
        prompt = (
            f"You are the official writer for the Knowledge-Based Currency (KBC) project.\n"
            f"Write a 600-word blog post for {today} on this topic: '{topic}'.\n"
            f"Include context on the concepts of Proof-of-Knowledge, K‑Chain, LightWeb, and Oracle AI, where appropriate.\n"
            f"The tone should be educational and forward-thinking. Do not include YAML front matter, code fences, or markdown headers."
        )

    response = client.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content.strip()


# ---- WRITING ----
def write_post(title: str, body: str) -> Path:
    date = datetime.date.today()
    slug = slugify(title)[:60]
    filename = Path("content/posts") / f"{date.isoformat()}-{slug}.md"
    filename.parent.mkdir(parents=True, exist_ok=True)

    front_matter = (
        f"---\n"
        f"title: \"{title.capitalize()}\"\n"
        f"date: {date.isoformat()}\n"
        f"draft: false\n"
        f"tags: [\"KBC\", \"daily-update\"]\n"
        f"---\n\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + body + "\n")

    return filename


# ---- MAIN ----
def main():
    client = get_openai_client()
    summary = read_chat_summary()
    index = datetime.date.today().timetuple().tm_yday % 15
    topic = "today's KBC update" if summary else choose_topic(index)
    post = generate_post(topic, client, summary)
    filepath = write_post(topic, post)
    print(f"✅ Blog post generated: {filepath}")


if __name__ == "__main__":
    main()
