from core.classes import LOCATION_NAMES
from core.saves import parse_saves
from core.timewise_logic import (
    get_location_times,
    get_offline_stats,
)


def analyse_save(save_text, location_values, player_index=0, event_loc=None):
    saves, save_count = parse_saves(save_text)
    if player_index >= save_count:
        raise ValueError(
            f"player_index {player_index} out of range ({save_count} players)"
        )

    save = saves[f"save_file_{player_index}"]

    stats = save["progress_data"]["quest_data"]["stats"]
    star_levels = save["progress_data"]["quest_data"]["star_levels"]
    player_level = save["player_level"]

    locations = get_location_times(stats)
    offline_stats = get_offline_stats(
        locations, location_values, star_levels, player_level, event_loc
    )

    return {
        "player_name": save.get("player_name"),
        "player_level": player_level,
        "locations": [
            {
                "name": LOCATION_NAMES[loc.name],
                "stars": loc.stars,
                "completed_in": loc.completed_in,
                "completed_in_best": loc.completed_in_best,
                "ends_in_death": loc.ends_in_death,
                "loops": loc.loops,
                "chests_per_run": loc.chests_per_run,
                "value_per_clear": loc.value_per_clear,
                "enchant_rate": loc.enchant_rate,
                "enchant_rate_best": loc.enchant_rate_best,
            }
            for loc in offline_stats.values()
        ],
    }
