import json
from pathlib import Path
from datetime import datetime, timezone

STATE_PATH = Path.home() / ".gitfish" / "state.json"
STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT = {
    "user": {
        "xp": 0,
        "coins": 0,
        "level": 1,
        "streak_days": 0,
        "streak_weeks": 0,
        "last_active_day": None
    },
    "gear": {
        "rod_level": 1,
        "luck_bonus": 0.0
    },
    "last_sync": None,
    "last_processed_event_id": None
}

def load_state():
    if not STATE_PATH.exists():
        save_state(DEFAULT)
        return DEFAULT.copy()
    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state: dict):
    if isinstance(state.get("last_sync"), datetime):
        state["last_sync"] = state["last_sync"].astimezone(timezone.utc).isoformat()
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
