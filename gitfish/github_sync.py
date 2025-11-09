import os
import requests
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


def fetch_recent_events(since_iso=None, per_page=100):
    params = {"per_page": per_page}
    resp = requests.get(EVENTS_URL, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def score_events(events):
    """Calculate XP and coins from events."""
    xp = 0
    coins = 0
    for event in events:
        event_type = event.get("type")
        score = SCORES.get(event_type)
        if score:
            xp += score["xp"]
            coins += score["coins"]
    return xp, coins


def sync_from_github(reset=False):
    """
    Sync GitHub activity and update XP/coins.
    
    Only processes events that haven't been seen before, tracked by event ID.
    
    Args:
        reset: If True, clear processed events list and process all recent events
    """
    state = load_state()
    
    # Get list of already processed event IDs
    processed_ids = set() if reset else set(state.get("processed_event_ids", []))
    
    # Fetch recent events from GitHub
    all_events = fetch_recent_events()
    
    # Filter to only new events (not already processed)
    new_events = [e for e in all_events if e.get("id") not in processed_ids]
    
    # Score the new events
    xp, coins = score_events(new_events)
    
    # Update state
    state["user"]["xp"] += xp
    state["user"]["coins"] += coins
    
    # Track all processed event IDs (both old and new)
    for event in new_events:
        event_id = event.get("id")
        if event_id:
            processed_ids.add(event_id)
    
    state["processed_event_ids"] = list(processed_ids)
    save_state(state)
    
    return {
        "xp": xp,
        "coins": coins,
        "events": len(new_events),
        "total_xp": state["user"]["xp"],
        "total_coins": state["user"]["coins"]
    }