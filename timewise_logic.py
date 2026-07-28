import re
from math import floor

from classes import LocOfflineStats, LocPlayerStats


def get_location_times(stats, locations):
    for location in stats:
        match = re.match(r"^([a-zA-Z_]+)(\d+)$", location["id"])

        if match:
            name, stars = match.groups()
        else:
            continue

        aHg_val = location.get("aHg", 0.0)
        aHl_val = location.get("aHl", 0.0)

        loc_stats = LocPlayerStats(
            loc_id=location["id"],
            name=name,
            stars=int(stars),
            bT=location.get("bT", 0.0),
            aT=location.get("aT", 0.0),
            aHl=aHl_val,
            aHg=aHg_val,
            net_hp=aHg_val - aHl_val,
            aKg=location.get("aKg", 0.0),
            aXg=location.get("aXg", 0.0),
            aRg=location.get("aRg", 0.0),
            d=location.get("d", 0.0),
        )
        locations[(name, int(stars))] = loc_stats


def get_max_runs(loc: LocPlayerStats, star_levels, player_level):

    max_unlocked = star_levels[loc.name]
    star_diff = max_unlocked - loc.stars
    max_hp = player_level + 20
    max_chests = player_level * 5 + 100
    # todo : check also current amount of chests

    guarantee = 0
    if star_diff >= 3:
        guarantee = 1
    elif star_diff == 2:
        guarantee = 2 / 3
    elif star_diff == 1:
        guarantee = 1 / 3

    chests_per_run = get_chests_per_run(loc)
    if loc.net_hp >= 0:
        runs_before_death = max_chests
    else:
        runs_before_death = max_hp // abs(loc.net_hp)

    chests = floor(guarantee * max_chests)

    runs = min(max(chests, runs_before_death * chests_per_run), 400)

    return runs


def get_completion_time(time, loops, chests_per_run=1):
    OROBOROUS_FRAMES = 118
    CHEST_FRAMES = 36

    treasures = loops * chests_per_run

    total_frames = (
        (time * loops) + (OROBOROUS_FRAMES * (loops - 1)) + (CHEST_FRAMES * treasures)
    )

    return total_frames


def get_chests_per_run(loc):
    if loc.name == "caustic_caves" and loc.stars >= 5 and loc.stars <= 15:
        return 2
    else:
        return 1

    # event logic too


def get_offline_stats(player_stats, location_values):
    pass
