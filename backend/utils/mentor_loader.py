import json
import os

def load_mentor(mentor_id: str):
    path = f"mentors/{mentor_id}.json"

    if not os.path.exists(path):
        path = "mentors/default.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
