import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from gitfish.state import load_state, save_state

# Load environment variables from .env file if it exists
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

EVENTS_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/events"

# basic scoring system for MVP, per event
SCORES = {
    "PushEvent": {"xp": 1, "coins": 1},
    "PullRequestEvent": {"xp": 5, "coins": 4},
    "PullRequestReviewEvent": {"xp": 3, "coins": 2},
    "IssuesEvent": {"xp": 2, "coins": 1},
    "CreateEvent": {"xp": 5, "coins": 3}
}


def fetch_events(since_iso=None, per_page=100):
    params = {"per_page": per_page}
    resp = requests.get(EVENTS_URL, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    events = resp.json()

    if since_iso:
        since_dt = datetime.fromisoformat(since_iso)
        events = [e for e in events if datetime.fromisoformat(
            e["created_at"].replace("Z", "+00:00")) > since_dt]
    return events


def score_events(events):
    xp = 0
    coins = 0
    for e in events:
        t = e.get("type")
        score = SCORES.get(t)
        if score:
            xp += score["xp"]
            coins += score["coins"]
    return xp, coins


def sync_from_github(reset=False):
    """
    Sync GitHub activity and update XP/coins.

    Args:
        reset: If True, ignore last_sync and process all recent events (useful if you made commits before last sync)
    """
    state = load_state()
    last_processed_event_time = None if reset else state.get("last_sync")
    last_processed_event_id = None if reset else state.get(
        "last_processed_event_id")

    events = fetch_events(since_iso=last_processed_event_time)

    if last_processed_event_id:
        events = [e for e in events if e.get("id") != last_processed_event_id]

    xp, coins = score_events(events)

    state["user"]["xp"] += xp
    state["user"]["coins"] += coins

    if events:
        most_recent_event = events[0]
        most_recent_event_time = most_recent_event["created_at"].replace(
            "Z", "+00:00")
        state["last_sync"] = most_recent_event_time
        state["last_processed_event_id"] = most_recent_event.get("id")

    save_state(state)
    return {"xp": xp, "coins": coins, "events": len(events), "total_xp": state["user"]["xp"], "total_coins": state["user"]["coins"]}

# test 2 1 1 1 1 1