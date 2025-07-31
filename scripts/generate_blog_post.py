#!/usr/bin/env python3
"""
generate_blog_post.py
----------------------

This script generates a new blog post for the KBC website using the OpenAI
ChatCompletion API.  It selects a random topic from a predefined list and
asks the language model to write a concise, engaging post that fits within
the Knowledge‑Based Currency project.  The resulting Markdown file is
written to the `content/posts/` directory with a timestamped filename and
front matter ready for Hugo.

To use this script:
1. Install the `openai` and `python-slugify` packages (see the GitHub
   Actions workflow in `.github/workflows/blog_automation.yml` for example).
2. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
3. Run the script from the root of the repository.

The script will do nothing if the `OPENAI_API_KEY` is not set.
"""

import os
import datetime
import random
from pathlib import Path

try:
    import openai  # type: ignore
except ImportError:
    raise SystemExit("The 'openai' package is required. Install it via pip install openai.")

try:
    from slugify import slugify  # type: ignore
except ImportError:
    raise SystemExit("The 'python-slugify' package is required. Install it via pip install python-slugify.")


def get_openai_client() -> "openai.Client":
    """Initialize the OpenAI client from the environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY environment variable not set. Cannot generate blog post.")
    openai.api_key = api_key
    return openai


def choose_topic() -> str:
    """Deterministically select the next topic from a 15-topic list, rotating twice per month."""
    topics = [
        "Introduction to Knowledge-Based Currency (KBC)",
        "Understanding the K-Chain: Immutable Knowledge Ledger",
        "How Oracle AI Validates Truth in KBC",
        "Decentralization: KBC’s Vision for the Future",
        "LightWeb Explained: Decentralized Knowledge Sharing",
        "Proof-of-Knowledge vs. Traditional Blockchain Proofs",
        "KBC's Impact on Education and Learning",
        "Integrating AI and Human Intelligence via KBC",
        "Knowledge Valuation: How KBC Measures Truth",
        "Economic Benefits of Knowledge-Based Currency",
        "Historical Influences that Inspired KBC",
        "Using KBC to Build a Trustworthy Internet",
        "The Mathematics Behind the KBC System",
        "Future Innovations and Potential of KBC",
        "How KBC Reinvents Community and Collaboration"
    ]

    today = datetime.date.today()
    run_number = 0 if datetime.datetime.utcnow().hour < 12 else 1  # 0 = midnight, 1 = noon
    index = ((today.timetuple().tm_yday - 1) * 2 + run_number) % len(topics)
    return topics[index]


def read_chat_summary() -> str | None:
    """Return the contents of a chat summary file if provided.

    If the environment variable `CHAT_SUMMARY_PATH` is set and points to
    a readable file, this function returns its contents.  This allows
    the daily post to summarize recent discussions or progress.  If
    the variable is not set or the file does not exist, returns None.
    """
    path = os.environ.get("CHAT_SUMMARY_PATH")
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def generate_post(topic: str, client: "openai", summary: str | None) -> str:
    """Call OpenAI API to generate a blog post."""
    today = datetime.date.today().strftime("%B %d")
    year = datetime.date.today().year
    if summary:
        prompt = (
            "You are an expert technical writer for the Knowledge-Based Currency (KBC) project.\n"
            f"Write a 600-word engaging blog post for {today}, {year}, based on this topic: {topic}.\n" summarizing today's progress on KBC.\n"
            f"Use these notes:\n{summary}\n\n"
            "Ensure the post is accessible to a general audience, maintains an inspirational tone, "
            "and clearly explains relevant KBC concepts such as verifiable knowledge, Proof-of-Knowledge, K-Chain, LightWeb, and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )
    else:
        prompt = (
            "You are an expert technical writer for the Knowledge-Based Currency (KBC) project.\n"
            f"Write a 600-word engaging blog post for {today}, making connections to important historical events on this date.\n"
            f"The specific topic is: {topic}.\n"
            "Ensure the post is accessible to a general audience, maintains an inspirational tone, "
            "and clearly explains relevant KBC concepts such as verifiable knowledge, Proof-of-Knowledge, K-Chain, LightWeb, and Oracle AI. "
            "Use headings and paragraphs. Do not include YAML front matter or code fences."
        )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()




def write_post(title: str, body: str) -> Path:
    """Write the generated post to a Markdown file with front matter."""
    date = datetime.date.today()
    slug = slugify(title)  # create a URL‑friendly filename
    posts_dir = Path("content/posts")
    posts_dir.mkdir(parents=True, exist_ok=True)
    filename = posts_dir / f"{date.isoformat()}-{slug}.md"
    front_matter = (
        f"---\n"
        f"title: \"{title.capitalize()}\"\n"
        f"date: {date.isoformat()}\n"
        f"draft: false\n"
        f"---\n\n"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(body)
        f.write("\n")
    return filename


def main() -> None:
    client = get_openai_client()
    # Read an optional chat summary for context; if unavailable, choose a random topic
    summary = read_chat_summary()
    if summary:
        topic = "today's KBC update"
    else:
        topic = choose_topic()
    content = generate_post(topic, client, summary)
    path = write_post(topic, content)
    print(f"Generated blog post at {path}")


if __name__ == "__main__":
    main()