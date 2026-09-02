import location_data
from classes import EVENT_LOCATIONS, LOCATION_INDEX, LOCATION_NAMES
from saves import get_save
from timewise_logic import (
    get_best_loc,
    get_completion_time_table,
    get_location_times,
    get_offline_stats,
)
from util import choose_number


def start():

    print(
        """
============================================================================
Hello and welcome to the sundial! to get started, choose a save file to analyze
(Note: Pressing "enter" or an invalid input defaults to the first option).
============================================================================"""
    )
    save = get_save()
    # TODO: add actual UX

    # TODO : debug mode stuff to see your save
    # with open("save_dump.json", "w", encoding="utf-8") as f:
    #     json.dump(save, f, indent=2)

    # TODO: allow the player to choose
    # path 1: get the optimal stats direclty here
    location_values = location_data.get_location_values()
    if location_values is None:
        print(
            "wasnt able to find the location values to calculate optimal location. want to do anything else with your save?"
        )
    else:
        stats: list = save["progress_data"]["quest_data"]["stats"]
        star_levels: list = save["progress_data"]["quest_data"]["star_levels"]
        player_level = save["player_level"]
        active_event_ids = (
            save["progress_data"]["quest_data"].get("events", {}).get("sIds", [])
        )

        event_bonus: bool = (
            input("""
====================================================================
Want to apply event bonus to any location? (y/N): """)
            == "y"
        )
        active_event_loc = None

        if event_bonus:
            if len(active_event_ids) != 0:
                loc_name = LOCATION_NAMES[EVENT_LOCATIONS[active_event_ids[0]]]

                if (
                    input(f"""
====================================================================
Detected active event: {active_event_ids}, {loc_name} gets 2X chests)
Apply this bonus? (Y/n): """)
                    != "n"
                ):
                    print(f"applying event bonus for {loc_name}")
                    active_event_loc = EVENT_LOCATIONS[active_event_ids[0]]

            if active_event_loc is None:
                chosen_id = choose_number(
                    message="""
====================================================================
Choose a location to apply event bonus to:
1. Rocky Plateau
2. Deadwood Canyon
3. Caves of Fear
4. Mushroom Forest
5. Haunted Halls
6. Boiling Mine
7. Icy Ridge
8. Temple
--------------------------------------------------------------------
0. Exit (default)
""",
                    retry=False,
                    default=0,
                    max=8,
                )

                LOC_INDEX_REV = {v: k for k, v in LOCATION_INDEX.items()}
                active_event_loc = LOC_INDEX_REV.get(chosen_id)

        locations = get_location_times(stats)

        offline_stats = get_offline_stats(
            locations, location_values, star_levels, player_level, active_event_loc
        )

        best = get_best_loc(offline_stats)

        if best is None:
            print(
                "Somehow, some way, you have no location that is possible to offline. Get good?"
            )
        else:
            print(
                f"your best location is: {LOCATION_NAMES[best[0]]} with {best[1]} stars"
            )
            # TODO: better formatting lol

        # path 2: output to timewise (local / web)
        # TODO implement this
        # path 3: get a copy paste for timewise
        table = get_completion_time_table(offline_stats, True)
        with open("completion_times.tsv", "w", encoding="utf-8") as f:
            f.write(table)


if __name__ == "__main__":
    start()
