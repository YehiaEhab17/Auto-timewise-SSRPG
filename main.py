import location_data
from classes import LocationStats
from saves import get_saves
from timewise_logic import get_completion_time, get_location_times, get_max_runs

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
    save: dict = get_saves()

    # todo: add actual UX

    # todo: let them choose which save to proceed with
    locations: dict[tuple[str, int], LocationStats] = {}
    stats: list = save["save_file_0"]["progress_data"]["quest_data"]["stats"]
    star_levels: list = save["save_file_0"]["progress_data"]["quest_data"][
        "star_levels"
    ]
    player_level = save["save_file_0"]["player_level"]
    get_location_times(stats, locations)

    runs = get_max_runs(locations["icy_ridge", 15], star_levels, player_level)
    print(runs)
    print(get_completion_time(locations["icy_ridge", 15].aT, runs))
    print(get_completion_time(locations["icy_ridge", 15].bT, runs))

    # path 1: get the optimal stats direclty here
    location_values = location_data.get_location_values()

    if location_values is None:
        print(
            "wasnt able to find the location values to calculate optimal location. want to do anything else with your save?"
        )
    else:
        pass

    # path 2: output to timewise (local / web)

    # path 3: get a copy paste for timewise


if __name__ == "__main__":
    start()
