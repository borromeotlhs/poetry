"""Rick and Morty weighted episode picker.

Usage:
    python rick_and_morty_picker.py

Features:
- Holds an internal season/episode catalog (seasons 1-8; season 1 has 11 episodes,
  all others have 10) and tracks how often each episode is selected.
- Uses inverse weighting based on selection counts so episodes picked less often are
  more likely to be chosen (weight = 1 / (count + 1)).
- On every run, randomly selects an episode, displays the choice, increments that
  episode's counter, and rewrites this script to persist the updated counters.

Hulu note: Hulu uses standard season/episode numbering (e.g., ``S03E05``), which
matches the codes shown by this picker.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List

EPISODES_BY_SEASON: Dict[int, List[str]] = {
    1: [f"S01E{num:02d}" for num in range(1, 12)],
    2: [f"S02E{num:02d}" for num in range(1, 11)],
    3: [f"S03E{num:02d}" for num in range(1, 11)],
    4: [f"S04E{num:02d}" for num in range(1, 11)],
    5: [f"S05E{num:02d}" for num in range(1, 11)],
    6: [f"S06E{num:02d}" for num in range(1, 11)],
    7: [f"S07E{num:02d}" for num in range(1, 11)],
    8: [f"S08E{num:02d}" for num in range(1, 11)],
}

# >>> COUNTS START
SELECTION_COUNTS: Dict[str, int] = {
    "S01E01": 1,
    "S01E02": 4,
    "S01E03": 1,
    "S01E04": 0,
    "S01E05": 1,
    "S01E06": 1,
    "S01E07": 1,
    "S01E08": 2,
    "S01E09": 1,
    "S01E10": 1,
    "S01E11": 1,
    "S02E01": 1,
    "S02E02": 2,
    "S02E03": 0,
    "S02E04": 0,
    "S02E05": 1,
    "S02E06": 2,
    "S02E07": 0,
    "S02E08": 0,
    "S02E09": 2,
    "S02E10": 1,
    "S03E01": 2,
    "S03E02": 1,
    "S03E03": 2,
    "S03E04": 1,
    "S03E05": 2,
    "S03E06": 1,
    "S03E07": 0,
    "S03E08": 1,
    "S03E09": 2,
    "S03E10": 1,
    "S04E01": 2,
    "S04E02": 1,
    "S04E03": 1,
    "S04E04": 1,
    "S04E05": 1,
    "S04E06": 1,
    "S04E07": 2,
    "S04E08": 1,
    "S04E09": 2,
    "S04E10": 2,
    "S05E01": 1,
    "S05E02": 2,
    "S05E03": 1,
    "S05E04": 1,
    "S05E05": 2,
    "S05E06": 1,
    "S05E07": 3,
    "S05E08": 2,
    "S05E09": 1,
    "S05E10": 1,
    "S06E01": 1,
    "S06E02": 0,
    "S06E03": 2,
    "S06E04": 4,
    "S06E05": 3,
    "S06E06": 0,
    "S06E07": 1,
    "S06E08": 1,
    "S06E09": 0,
    "S06E10": 1,
    "S07E01": 1,
    "S07E02": 0,
    "S07E03": 1,
    "S07E04": 2,
    "S07E05": 2,
    "S07E06": 0,
    "S07E07": 1,
    "S07E08": 2,
    "S07E09": 1,
    "S07E10": 1,
    "S08E01": 1,
    "S08E02": 1,
    "S08E03": 1,
    "S08E04": 1,
    "S08E05": 1,
    "S08E06": 1,
    "S08E07": 1,
    "S08E08": 1,
    "S08E09": 1,
    "S08E10": 2
}
# <<< COUNTS END


def flatten_catalog() -> List[str]:
    return [episode for episodes in EPISODES_BY_SEASON.values() for episode in episodes]


def ensure_counts_complete() -> None:
    catalog = set(flatten_catalog())
    missing = catalog.difference(SELECTION_COUNTS)
    for episode in missing:
        SELECTION_COUNTS[episode] = 0
    for episode in list(SELECTION_COUNTS):
        if episode not in catalog:
            del SELECTION_COUNTS[episode]


def weighted_choice(episodes: List[str]) -> str:
    weights = [1 / (SELECTION_COUNTS.get(ep, 0) + 1) for ep in episodes]
    return random.choices(episodes, weights=weights, k=1)[0]


def save_counts() -> None:
    path = Path(__file__)
    content = path.read_text(encoding="utf-8")
    start_marker = "# >>> COUNTS START"
    end_marker = "# <<< COUNTS END"
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    if start_index == -1 or end_index == -1:
        raise SystemExit("Could not locate counter markers in script for self-update.")

    serialized = json.dumps(SELECTION_COUNTS, indent=4, sort_keys=True)
    replacement = f"{start_marker}\nSELECTION_COUNTS: Dict[str, int] = {serialized}\n{end_marker}"

    new_content = content[:start_index] + replacement + content[end_index + len(end_marker) :]
    path.write_text(new_content, encoding="utf-8")


def main() -> None:
    ensure_counts_complete()
    episodes = flatten_catalog()
    selection = weighted_choice(episodes)
    SELECTION_COUNTS[selection] = SELECTION_COUNTS.get(selection, 0) + 1
    print(f"Selected episode: {selection} (selected {SELECTION_COUNTS[selection]} time(s))")
    save_counts()


if __name__ == "__main__":
    main()
