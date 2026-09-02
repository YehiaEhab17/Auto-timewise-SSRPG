from cli.saves import get_save
from cli.util import choose_number, copy_to_clipboard, parse_afk_time
from cli.xlsx_data import get_location_values
from core.classes import EVENT_LOCATIONS, LOCATION_INDEX, LOCATION_NAMES
from core.timewise_logic import (
    get_completion_time_table,
    get_location_times,
    get_offline_stats,
    get_timewise_formatted_time,
    sort_locs_by_rate,
)


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

    # path 1: get the optimal stats direclty here
    location_values = get_location_values()
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
                    max_val=8,
                )

                LOC_INDEX_REV = {v: k for k, v in LOCATION_INDEX.items()}
                active_event_loc = LOC_INDEX_REV.get(chosen_id)

        locations = get_location_times(stats)

        offline_stats = get_offline_stats(
            locations, location_values, star_levels, player_level, active_event_loc
        )

        sorted_avg = sort_locs_by_rate(offline_stats, False)
        sorted_best = sort_locs_by_rate(offline_stats, True)

        if not sorted_avg:
            print(
                "Somehow, some way, you have no location that is possible to offline. Get good?"
            )
        else:
            best = sorted_avg[0]
            best_bt = sorted_best[0]

            readable_time = get_timewise_formatted_time(best.completed_in)
            readable_time_bt = get_timewise_formatted_time(best.completed_in_best)

            print("""
=============================================================================
How long will you AFK for? 
(format as HH:MM, enter 0 to get the best location generally)
""")
            afk_time_str = input("AFK time: ")
            afk_time = parse_afk_time(afk_time_str)
            best_afk = None
            if afk_time:
                lowest = None
                for loc in sorted_avg:
                    if lowest is None or loc.completed_in < lowest.completed_in:
                        lowest = loc
                    if loc.completed_in > afk_time * 30:
                        continue
                    best_afk = loc
                    break
                if best_afk is None:
                    best_afk = lowest

            print(f"""
=============================================================================
Based on your average times, your best location is: {LOCATION_NAMES[best.name]} with {best.stars} stars
Your run will complete in {readable_time[0]:.0f}h{readable_time[1]:.0f}m, with a rate of 1 enchant point per {1 / best.enchant_rate:.2f} seconds
{"your run ends in death" if best.ends_in_death else "your run does not end in death"}

Based on your best times, your best location is: {LOCATION_NAMES[best_bt.name]} with {best_bt.stars} stars
Your run will complete in {readable_time_bt[0]:.0f}h{readable_time_bt[1]:.0f}m, with a rate of 1 enchant point per {1 / best_bt.enchant_rate_best:.2f} seconds
{"your run ends in death" if best_bt.ends_in_death else "your run does not end in death"}""")

            if best_afk:
                readable_time_afk = get_timewise_formatted_time(best_afk.completed_in)
                print(f"""
=============================================================================
Based on your AFK time ({afk_time_str}), your best location is: {LOCATION_NAMES[best_afk.name]} with {best_afk.stars} stars
Your run will complete in {readable_time_afk[0]:.0f}h{readable_time_afk[1]:.0f}m, with a rate of 1 enchant point per {1 / best_afk.enchant_rate:.2f} seconds
{"your run ends in death" if best_afk.ends_in_death else "your run does not end in death"}
=============================================================================
""")

            print("""
=============================================================================
Top 5 locations based on best times (targets for optimisation):""")
            for i in range(min(5, len(sorted_best))):
                loc = sorted_best[i]
                readable_time = get_timewise_formatted_time(loc.completed_in_best)
                print(
                    f"{i + 1}. {LOCATION_NAMES[loc.name]}: {loc.stars}*. {readable_time[0]:.0f}h{readable_time[1]:.0f}m {'(death)' if loc.ends_in_death else ''}. {1 / loc.enchant_rate_best:.2f}s for 1EP"
                )

        # path 2: output to timewise (local / web)
        # TODO implement this

        # path 3: get a copy paste for timewise
        if (
            input(
                """
=============================================================================
Do you want to copy the completion times to your clipboard (to paste into timewise)? (y/N): """
            )
            == "y"
        ):
            table = get_completion_time_table(offline_stats, True)
            if copy_to_clipboard(table):
                print("Copied to clipboard!")
            else:
                print(
                    "Failed to copy to clipboard. Output to .tsv (for importing into sheets)? (y/N): "
                )
                if input() == "y":
                    with open("completion_times.tsv", "w", encoding="utf-8") as f:
                        f.write(table)
                else:
                    print("Skipping output to .tsv.")


if __name__ == "__main__":
    start()
