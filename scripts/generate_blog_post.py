#!/usr/bin/env python3
"""
Generate a daily blog post for the KBC site.

If CHAT_SUMMARY_PATH points to a text file, its contents are used as context.
Otherwise, the script chooses a topic from a rotating list. It writes a Markdown file
with Hugo front matter into content/posts/.
"""
import os
import random
import datetime
from pathlib import Path
from slugify import slugify
from openai import OpenAI  # OpenAI v1 client

def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def read_chat_summary() -> str | None:
    path = os.environ.get("CHAT_SUMMARY_PATH")
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None

def get_topic_by_day() -> str:
    topics = [
        "the philosophy behind Knowledge-Based Currency",
        "how the K-Chain ensures trust and immutability",
        "the vision of LightWeb as a decentralized knowledge internet",
        "the role of Oracle AI in validating and synthesizing knowledge",
        "the mathematics and mechanics of KBC",
        "how knowledge becomes a universal asset",
        "why KBC matters for science and innovation",
        "the future of decentralized learning and value",
        "how KBC combats misinformation and preserves truth",
        "incentives for collaboration and contribution in KBC",
        "how the KBC ledger ensures transparency and fairness",
        "KBC and education: building the next generation of thinkers",
        "applying KBC principles in real-world institutions",
        "KBC's approach to intellectual property and authorship",
        "how KBC aligns with the natural growth of knowledge"
    ]
    day_index = datetime.date.today().day % len(topics)
    return topics[day_index]

def generate_post(topic: str, client: OpenAI, summary: str | None) -> str:
    if summary:
        prompt = (
            "You are an expert technical writer for the Knowledge-Based Currency (KBC) project.\n"
            "Write a 600-word blog post summarizing today's progress on the KBC project.\n"
            "Use the following notes as context:\n"
            f"{summary}\n\n"
            "Ensure the post is accessible to a general audience, maintains a positive and inspirational tone, "
            "and explains relevant KBC concepts such as verifiable knowledge, Proof-of-Knowledge, K-Chain, LightWeb and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )
    else:
        prompt = (
            "You are an expert technical writer for the Knowledge-Based Currency (KBC) project.\n"
            f"Write a 600-word blog post about {topic}.\n"
            "The post should be accessible to a general audience, maintain a positive and inspirational tone, "
            "and explain the core ideas of KBC: verifiable knowledge, Proof-of-Knowledge, K-Chain, LightWeb and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def write_post(title: str, body: str) -> Path:
    date = datetime.date.today()
    posts_dir = Path("content/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    filename = posts_dir / f"{date.isoformat()}-{slug}.md"
    front_matter = (
        f"---\n"
        f"title: \"{title.capitalize()}\"\n"
        f"date: {date.isoformat()}\n"
        f"draft: false\n"
        f"tags: [\"KBC\", \"daily-updates\"]\n"
        f"---\n\n"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + body + "\n")
    return filename

def main() -> None:
    client = get_openai_client()
    summary = read_chat_summary()
    topic = "today's KBC update" if summary else get_topic_by_day()
    body = generate_post(topic, client, summary)
    path = write_post(topic, body)
    print(f"Generated blog post: {path}")

if __name__ == "__main__":
    main()