#!/usr/bin/env python3
"""
Automated blog post generator for the Knowledge‑Based Currency (KBC) website.

This script rotates through a list of topics defined in ``scripts/topics.json``,
fetches recent news headlines related to the selected topic, constructs a
prompt that directs a language model to write a concise, well‑structured post
about the topic, and saves the resulting content as a Markdown file with
Hugo‑style front matter.

Environment variables required:

* ``OPENAI_API_KEY`` – API key for OpenAI's ChatCompletion endpoint.
* ``NEWS_API_KEY``   – API key for your preferred news provider (e.g. NewsAPI.org).

The script maintains a simple state file (``scripts/.blog_state.json``) to
remember which topics have been used recently. When run with ``--rotate`` it
avoids repeating a topic within the cooldown window (default: 21 days).

Usage (from repository root):
    python scripts/generate_blog_post.py --rotate --cooldown-days 21

If ``--rotate`` is omitted, a random topic will be selected from the list.
"""

import argparse
import datetime
import json
import os
import random
import requests
from pathlib import Path

import openai
from slugify import slugify

# Determine project directories relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / "content" / "posts"
TOPICS_FILE = SCRIPT_DIR / "topics.json"
STATE_FILE = SCRIPT_DIR / ".blog_state.json"

# Configure API keys from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please add it to your repository secrets or local environment."
    )

openai.api_key = OPENAI_API_KEY


def load_topics() -> list[str]:
    """Load the list of topics from the JSON file."""
    try:
        data = json.loads(TOPICS_FILE.read_text(encoding="utf-8"))
        topics = data.get("topics") or data
        if not isinstance(topics, list):
            raise ValueError("Topics file must contain a JSON array or {'topics': [...]} format")
        return topics
    except FileNotFoundError:
        raise FileNotFoundError(f"Topics file not found: {TOPICS_FILE}")


def load_state() -> dict:
    """Load state from the state file; return empty dict if file missing."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    """Persist state to the state file."""
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def choose_topic(topics: list[str], cooldown_days: int, state: dict) -> str:
    """Select a topic respecting the cooldown window when ``--rotate`` is used."""
    if cooldown_days <= 0:
        return random.choice(topics)
    # Determine topics used within the cooldown window
    cutoff = datetime.date.today() - datetime.timedelta(days=cooldown_days)
    recent = {
        entry["topic"]
        for entry in state.get("history", [])
        if datetime.date.fromisoformat(entry["date"]) >= cutoff
    }
    # Filter out recent topics; if all topics used, ignore cooldown
    available = [t for t in topics if t not in recent]
    return random.choice(available or topics)


def fetch_recent_news(query: str, max_articles: int = 3) -> list[str]:
    """Fetch recent news headlines about the topic using a news API.

    The returned list contains markdown list items: ``- Title (URL)``.
    If no API key is configured or no articles are found, returns an empty list.
    """
    if not NEWS_API_KEY:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY,
        "language": "en",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        items = []
        for article in articles:
            title = article.get("title", "News article")
            url = article.get("url", "")
            if url:
                items.append(f"- {title} ({url})")
        return items
    except Exception as exc:
        # If the API request fails, return empty list; don't break generation
        print(f"Warning: could not fetch news for '{query}': {exc}")
        return []


def generate_post_body(topic: str, news_items: list[str]) -> str:
    """Call OpenAI to generate a blog post body for the given topic."""
    # Build the prompt detailing structure, tone and including news items
    news_section = "\n".join(news_items) if news_items else "No recent news available."
    prompt = (
        f"You are a knowledgeable technical writer for the Knowledge‑Based Currency (KBC) project.\n"
        f"Write a blog post about the topic **{topic}**. Start with a concise overview of the topic "
        f"and why it matters to KBC. Then include a section titled 'Recent News' summarising the following "
        f"bullet points (if any), using them to inform the narrative:\n{news_section}\n\n"
        f"Use Markdown formatting throughout: include level‑2 headings (##) for each section, such as 'Overview', 'Recent News', "
        f"and 'Conclusion'. Use bullet points to list the news headlines. In the conclusion, connect the topic back to the "
        f"broader KBC ecosystem and suggest questions for readers. Write in a clear, friendly tone for technically curious readers."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.6,
        n=1,
    )
    return response.choices[0].message["content"].strip()


def save_markdown(title: str, topic: str, body: str) -> Path:
    """Save the generated post to the ``content/posts`` directory as a Markdown file."""
    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    # Front matter with categories, tags and topic metadata
    front_matter = (
        f"---\n"
        f"title: \"{title}\"\n"
        f"date: {now_utc}\n"
        f"draft: false\n"
        f"tags: [\"KBC\", \"{topic.split()[0]}\"]\n"
        f"categories: [\"KBC\"]\n"
        f"topic: \"{topic}\"\n"
        f"---\n"
    )
    # Ensure content directory exists
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    # Construct a slug using the date and topic; truncate to avoid long filenames
    slug_base = slugify(f"{datetime.date.today()} {topic}")[:80]
    filename = f"{slug_base}.md"
    post_path = CONTENT_DIR / filename
    # Avoid overwriting existing files by incrementing suffix
    counter = 2
    while post_path.exists():
        post_path = CONTENT_DIR / f"{slug_base}-{counter}.md"
        counter += 1
    # Write the file
    post_path.write_text(front_matter + "\n" + body + "\n", encoding="utf-8")
    return post_path


def update_state(state: dict, topic: str) -> None:
    """Record the generated topic in history for cooldown rotation."""
    today_str = datetime.date.today().isoformat()
    state.setdefault("history", []).append({"topic": topic, "date": today_str})
    # Keep at most 180 entries to avoid unbounded growth
    state["history"] = state["history"][-180:]
    save_state(state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and save a blog post for KBC.")
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="Rotate topics, avoiding those used in the recent past (within cooldown).",
    )
    parser.add_argument(
        "--cooldown-days",
        type=int,
        default=21,
        help="Number of days to exclude recently used topics when rotating.",
    )
    args = parser.parse_args()

    topics = load_topics()
    state = load_state()

    # Choose a topic based on rotation or random selection
    topic = choose_topic(topics, args.cooldown_days if args.rotate else 0, state)
    # Fetch news and generate post content
    news_items = fetch_recent_news(topic)
    body = generate_post_body(topic, news_items)
    # Prepare title and write file
    title = f"{topic} — Daily KBC Note ({datetime.date.today().isoformat()})"
    post_path = save_markdown(title, topic, body)
    # Update state for rotation
    update_state(state, topic)
    print(f"Generated post: {post_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
