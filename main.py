import location_data
import json
from saves import get_save
from timewise_logic import (
    get_best_loc,
    get_completion_time_table,
    get_location_times,
    get_offline_stats,
)

# LOCATIONS = {
#     "rocky_plateau": "Rocky Plateau",
#     "deadwood_valley": "Deadwood Canyon",
#     "caustic_caves": "Caves of Fear",
#     "fungus_forest": "Mushroom Forest",
#     "undead_crypt": "Haunted Halls",
#     "bronze_mine": "Boiling Mine",
#     "icy_ridge": "Icy Ridge",
#     "temple": "Temple",
# }


def start():
    save = get_save()
    # TODO: add actual UX
    print(save)
    with open("save_dump.json", "w", encoding="utf-8") as f:
        json.dump(save, f, indent=2)
    # path 1: get the optimal stats direclty here
    location_values = location_data.get_location_values()
    if location_values is None:
        print(
            "wasnt able to find the location values to calculate optimal location. want to do anything else with your save?"
        )
    else:
        stats: list = save["progress_data"]["quest_data"]["stats"]

        locations = get_location_times(stats)

        star_levels: list = save["progress_data"]["quest_data"]["star_levels"]
        player_level = save["player_level"]

        offline_stats = get_offline_stats(
            locations, location_values, star_levels, player_level
        )

        best = get_best_loc(offline_stats)
        print(f"your best location is: {best}")

        # path 2: output to timewise (local / web)

        # path 3: get a copy paste for timewise
        table = get_completion_time_table(offline_stats, True)
        with open("completion_times.tsv", "w", encoding="utf-8") as f:
            f.write(table)


if __name__ == "__main__":
    start()
