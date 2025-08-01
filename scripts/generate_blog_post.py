#!/usr/bin/env python3
"""
Generate a blog post for the KBC site.  This script is designed to
be run automatically via GitHub Actions.  It will read an optional
daily summary file specified by the CHAT_SUMMARY_PATH environment
variable; if present, the summary will be used as context for the
post.  Otherwise, the script will choose a random topic from a list
of KBC themes and generate an ~600-word article using the OpenAI API.

Requires the following environment variables:

  OPENAI_API_KEY      – API key for OpenAI's Chat API
  CHAT_SUMMARY_PATH   – (optional) path to a text file with a summary
                         of recent KBC discussions; ignored if not set

Outputs a Markdown file into `content/posts/` with proper Hugo front
matter and a filename based on today's date and the slugified title.
"""
import os
import random
import datetime
from pathlib import Path
from slugify import slugify
from openai import OpenAI


TOPICS = [
    "the philosophy behind Knowledge‑Based Currency",
    "how the K‑Chain ensures trust and immutability",
    "the vision of LightWeb as a decentralized knowledge internet",
    "the role of Oracle AI in validating and synthesizing knowledge",
    "the mathematics and mechanics of KBC",
    "how knowledge becomes a universal asset",
    "why KBC matters for science and innovation",
    "the future of decentralized learning and value",
    "Proof‑of‑Knowledge and why it underpins KBC",
    "the role of IPv6 in the KnowledgeChain",
    "how KBC rewards contributors fairly",
    "bridging traditional finance with Knowledge‑Based Currency",
    "governance and decentralization in KBC",
    "education and learning incentives in the LightWeb",
    "how Oracle AI combats misinformation and bias"
]


def get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


def read_summary() -> str | None:
    path = os.environ.get("CHAT_SUMMARY_PATH")
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def choose_topic() -> str:
    return random.choice(TOPICS)


def generate_post(client: OpenAI, topic: str, summary: str | None) -> str:
    if summary:
        prompt = (
            "You are an expert technical writer for the Knowledge‑Based Currency (KBC) project.\n"
            "Write a 600-word blog post summarizing today's progress on the KBC project.\n"
            f"Use the following notes as context:\n{summary}\n\n"
            "Ensure the post is accessible to a general audience, maintains a positive and inspirational tone, "
            "and explains relevant KBC concepts such as verifiable knowledge, Proof‑of‑Knowledge, K‑Chain, LightWeb and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )
        title = "today's KBC update"
    else:
        prompt = (
            "You are an expert technical writer for the Knowledge‑Based Currency (KBC) project.\n"
            f"Write a 600-word blog post about {topic}.\n"
            "The post should be accessible to a general audience, maintain a positive and inspirational tone, "
            "and explain the core ideas of KBC: verifiable knowledge, Proof‑of‑Knowledge, K‑Chain, LightWeb and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )
        title = topic
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    return title, response.choices[0].message.content.strip()


def write_post(title: str, body: str) -> Path:
    date = datetime.date.today()
    posts_dir = Path("content/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)[:40]  # limit slug length
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
    client = get_client()
    summary = read_summary()
    if summary:
        topic = "today's KBC update"
    else:
        topic = choose_topic()
    title, body = generate_post(client, topic, summary)
    path = write_post(title, body)
    print(f"Generated {path}")


if __name__ == "__main__":
    main()